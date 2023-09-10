from pathlib import Path

from antievil import (
    LogicError,
    TypeExpectError,
    UnsupportedError,
)

from clyjin_templates.filesystem.models import (
    FileNode,
    FileNodeInternal,
    NodeContent,
    NodeFieldValue,
    NodeRoot,
    NodeType,
)
from clyjin_templates.template.group import TemplateGroup, TemplateGroupInternal
from clyjin_templates.utils.klass import Static
from clyjin_templates.utils.never import never


class TemplateGroupConversionUtils(Static):
    """
    Converts external Template Group to internal variant.
    """
    @staticmethod
    def convert_to_internal(group: TemplateGroup) -> TemplateGroupInternal:
        pass


class FileNodeConversionUtils(Static):
    """
    Converts external FileTreeNodes to internal variants.
    """
    @staticmethod
    def convert_to_internal(node: FileNode) -> FileNodeInternal:
        root: NodeRoot | None = node.root
        _type: NodeType | None = FileNodeConversionUtils._get_node_type(root)

        content: NodeContent | None = None
        if root is not None:
            content = FileNodeConversionUtils._get_node_content(
                root,
                _type,
            )

        nodes: dict[str, FileNodeInternal] | None = \
            FileNodeConversionUtils._convert_nodes(node)
        final_type: NodeType = FileNodeConversionUtils._get_final_type(
            _type,
            content,
            nodes
        )

        return FileNodeInternal(
            type=final_type,
            content=content,
            nodes=nodes,
        )

    @staticmethod
    def _get_final_type(
        pretype: NodeType | None,
        content: NodeContent | None,
        nodes: dict[str, FileNodeInternal] | None,
    ) -> NodeType:
        """
        Finds final type out of existing node parameters.

        If pretype is not None, it is returned. Otherwise guess depending on
        other given arguments is made, according to conventional defaults.
        """
        if pretype is not None:
            return pretype

        if content is None and nodes is None:
            # empty file assumed
            return NodeType.File
        if content is None and nodes is not None:
            return NodeType.Dir
        if content is not None and nodes is None:
            return NodeType.File
        if content is not None and nodes is not None:
            errmsg: str = \
                f"unexpected defined content=<{content}> and" \
                f" nodes=<{nodes}> at the same parent node"
            raise LogicError(errmsg)

        errmsg: str = "not all branches are considered"
        raise LogicError(errmsg)

    @staticmethod
    def _get_node_type(
        root: NodeRoot | None,
    ) -> NodeType | None:
        if root is None:
            return NodeType.Dir

        _type: NodeFieldValue | None = root.get("$type", None)

        if isinstance(_type, str):
            _type = NodeType(_type)

        if _type is None:
            # at this points we cannot recognize which type a node should have,
            # if it will have any subnodes - we would set directory, otherwise
            # file. Further conversion operations should handle this.
            return None
        elif not isinstance(_type, NodeType):
            raise TypeExpectError(
                obj=_type,
                ExpectedType=NodeType,
                expected_inheritance="instance",
                ActualType=type(_type),
            )
        return _type

    @staticmethod
    def _get_node_content(
        root: NodeRoot,
        _type: NodeType | None,
    ) -> NodeContent | None:
        content: NodeFieldValue | None = root.get("$content", None)

        if content is None:
            return None

        match _type:
            case NodeType.File:
                return FileNodeConversionUtils._get_file_node_content(content)
            case NodeType.Dir:
                # content is not None and type is Dir => directories can't
                # have content field
                raise UnsupportedError(
                    title="`$content` field for node of type",
                    value=_type,
                )
            case None:
                # content is not None and type is None, assuming file
                return FileNodeConversionUtils._get_file_node_content(content)
            case _:
                never(_type)
                return None

    @staticmethod
    def _get_file_node_content(
        maybe_content: NodeFieldValue,
    ) -> NodeContent:
        if not isinstance(maybe_content, (str, Path)):
            raise TypeExpectError(
                obj=maybe_content,
                # TODO(ryzhovalex): multiple ExpectedTypes as soon as
                #   Antievil supports it
                # 0
                ExpectedType=str,
                expected_inheritance="instance",
                ActualType=type(maybe_content),
            )

        return maybe_content

    @staticmethod
    def _convert_nodes(
        node: FileNode,
    ) -> dict[str, FileNodeInternal] | None:
        if node.root is None:
            return None

        result: dict[str, FileNodeInternal] = {}
        for k, v in node.root.items():
            if isinstance(v, FileNode):
                result[k] = FileNodeConversionUtils.convert_to_internal(v)

        if not result:
            return None
        return result
