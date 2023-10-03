import asyncio
from pathlib import Path
from typing import TYPE_CHECKING

import aiofiles
from antievil import (
    TypeExpectError,
    UnsetValueError,
)
from antievil.utils import never
from clyjin.log import Log
from mako.template import Template as MakoTemplate

from clyjin_templates.conversion import FileNodeConversionUtils
from clyjin_templates.filesystem.models import (
    FileNodeInternal,
    NodeContent,
    NodeType,
)
from clyjin_templates.template.vars import (
    TemplateGroupVar,
    TemplateGroupVarScope,
    TemplateGroupVarSpecialScope,
    TemplateGroupVarValue,
)

if TYPE_CHECKING:
    from clyjin_templates.template.group import TemplateGroup


class FileNodeMaker:
    """
    Makes files and directories out of template nodes.

    Args:
        templates_dir:
            Where to fetch templates referred by template group.
        template_group:
            Template group to create nodes from.
        target_dir:
            Where to save generated files and directories.
    """
    def __init__(
        self,
        *,
        templates_dir: Path,
        template_group: "TemplateGroup",
        target_dir: Path,
    ) -> None:
        self._templates_dir: Path = templates_dir
        self._template_group: "TemplateGroup" = template_group
        self._target_dir: Path = target_dir

    async def make(self) -> None:
        """
        Executes template group saving according files and directories to
        chosen dir.
        """
        Log.info(
            "[clyjin_templates.filesystem] making file tree for"
            f" template <{self._template_group.name}>"
            f" in dir <{self._target_dir}>",
        )
        internal_root_node: FileNodeInternal = \
            FileNodeConversionUtils.convert_to_internal(
                self._template_group.tree,
            )

        await self._make_subnodes(internal_root_node)

    async def _make_subnodes(
        self, host_node: FileNodeInternal,
    ) -> None:
        subnodes: dict[str, FileNodeInternal] | None = \
            host_node.nodes
        if subnodes is None:
            raise UnsetValueError(
                explanation="cannot initialize root node subnodes",
            )

        await asyncio.gather(*[
            self._make_node(
                node, node_name,
            ) for node_name, node in subnodes.items()
        ])

    async def _make_node(
        self,
        node: FileNodeInternal,
        node_name: str,
    ) -> None:
        match node.type:
            case NodeType.File:
                await self._make_file_node(node, node_name)
            case NodeType.Dir:
                await self._make_dir_node(node, node_name)
            case _:
                never(node.type)

    async def _make_file_node(
        self,
        node: FileNodeInternal,
        node_name: str,
    ) -> None:
        final_path: Path = Path(
            self._target_dir,
            node_name,
        )

        # to avoid unexpected overwriting, file shouldn't exist
        if final_path.exists():
            errmsg: str = f"file=<{final_path}> exists"
            raise FileExistsError(errmsg)

        final_content: str = await self._get_final_content(node.content)

        async with aiofiles.open(final_path, "w") as f:
            await f.write(final_content)

    async def _get_final_content(
        self,
        node_content: NodeContent | None,
    ) -> str:
        """
        Transform whatever is in node content into final writeable string.

        For all types of node content, Mako is called to evaluate in-content
        expressions.

        For None content, an empty string is returned.
        """
        if node_content is None:
            return ""

        raw_content: str = await self._get_raw_content_string(node_content)

        # TODO(ryzhovalex): temporarily All scope is used
        final_vars: dict[str, TemplateGroupVarValue] = \
            self._get_final_vars(TemplateGroupVarSpecialScope.All)

        return str(MakoTemplate(raw_content, output_encoding="utf-8").render(
            **final_vars,
        ))

    def _get_final_vars(
        self,
        scope: TemplateGroupVarScope,
    ) -> dict[str, TemplateGroupVarValue]:
        """
        Parses template group vars
        """
        # TODO(ryzhovalex): caching of vars per scope within the class

        if not self._template_group.vars:
            return {}

        vars_dump: dict[str, TemplateGroupVar | None] = \
            self._template_group.vars.model_dump()
        final_vars: dict[str, TemplateGroupVarValue] = {}

        for _var_name, _var_value in vars_dump.items():
            final_vars[_var_name] = _var_value

        return final_vars

    async def _get_raw_content_string(
        self, node_content: NodeContent,
    ) -> str:
        if isinstance(node_content, Path):
            async with aiofiles.open(node_content, "r") as f:
                return await f.read()
        elif isinstance(node_content, str):
            if node_content and node_content[0] == "&":
                return await self._get_template_raw_content_by_ref(
                    node_content,
                )

            return node_content

        raise TypeExpectError(
            obj=node_content,
            ExpectedType=str,
            expected_inheritance="instance",
            ActualType=type(node_content),
        )

    async def _get_template_raw_content_by_ref(
        self,
        ref: str,
    ) -> str:
        # remove leading ampersand
        parsed_ref: str = ref[1:]

        template_path: Path = Path(
            self._templates_dir,
            parsed_ref + ".mako",
        )

        async with aiofiles.open(template_path, "r") as f:
            return await f.read()

    async def _make_dir_node(
        self,
        node: FileNodeInternal,
        node_name: str,
    ) -> None:
        final_path: Path = Path(
            self._target_dir,
            node_name,
        )
        # folder intended to be created shouldn't exist. Maybe it will be
        # changed later but we want more strict behaviour for now.
        final_path.mkdir(parents=False, exist_ok=False)

        await self._make_subnodes(node)
