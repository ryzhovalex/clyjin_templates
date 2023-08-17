from pathlib import Path
from antievil import ExpectedTypeError, PleaseDefineError, UnsupportedError
from clyjin.log import Log
from mako.template import Template as MakoTemplate
from clyjin_templates.filetree.node import FileTreeNode, FileTreeNodeInternal
from clyjin_templates.filetree.types import NodeContent, NodeFieldValue, NodeRoot, NodeType
from clyjin_templates.template.group import TemplateGroup
from clyjin_templates.template.refname import RefTemplateName


class FileMaker:
    """
    Makes files and directories out of templates.
    """
    def __init__(self) -> None:
        pass

    async def make(
        self,
        template_group: TemplateGroup,
        target_dir: Path
    ) -> None:
        """
        Executes template group saving according files and directories to
        chosen dir.

        Args:
            template_group:
                Group to execute.
            target_dir:
                Where to save generated files and directories.
        """
        Log.info(
            "[clyjin_templates] making file tree for"
            f" template <{template_group.name}>"
            f" in dir <{target_dir}>"
        )

    async def _make_node(
        self,
        node: FileTreeNodeInternal
    )
