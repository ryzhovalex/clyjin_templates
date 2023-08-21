from clyjin_templates.filetree.node import FileTreeNode
from pathlib import Path
from antievil import TypeExpectError, PleaseDefineError, UnsupportedError
from clyjin.log import Log
from clyjin_templates.utils.never import never
from mako.template import Template as MakoTemplate
from clyjin_templates.filetree.node import FileTreeNode, FileTreeNodeInternal
from clyjin_templates.filetree.types import NodeContent, NodeFieldKey, NodeFieldValue, NodeRoot, NodeType
from clyjin_templates.template.group import TemplateGroup
from clyjin_templates.template.refname import RefTemplateName


class InternalFileTreeNodeConverter:
    """
    Converts external FileTreeNodes to internal variants.
    """
    def convert(
        self,
        node: FileTreeNode
    ) -> FileTreeNodeInternal:

        root: NodeRoot | None = node.root
        _type: NodeType = self._get_node_type(root)

        content: NodeContent | None = None
        if root is not None:
            content = self._get_node_content(
                root,
                _type
            )

        return FileTreeNodeInternal(
            type=_type,
            content=content,
            nodes=self._convert_nodes(node)
        )

    def _get_node_type(
        self,
        root: NodeRoot | None
    ) -> NodeType:
        if root is None:
            return NodeType.Dir

        _type: NodeFieldValue | None = root["$type"]

        if _type is None:
            return NodeType.File
        elif not isinstance(_type, NodeType):
            raise TypeExpectError(
                obj=_type,
                ExpectedType=NodeType,
                expected_inheritance="instance",
                ActualType=type(_type)
            )
        return _type

    def _get_node_content(
        self,
        root: NodeRoot,
        _type: NodeType
    ) -> NodeContent | None:
        content: NodeFieldValue | None = root["$content"]

        match _type:
            case NodeType.File:
                if content is None:
                    raise PleaseDefineError(
                        cannot_do="file-type node initializing",
                        please_define="`$content` field"
                    )
                elif not isinstance(content, (str, Path)):
                    raise TypeExpectError(
                        obj=content,
                        # TODO(ryzhovalex): multiple ExpectedTypes as soon as
                        #   Antievil supports it
                        # 0
                        ExpectedType=str,
                        expected_inheritance="instance",
                        ActualType=type(content)
                    )

                return content

            case NodeType.Dir:
                if content is not None:
                    raise UnsupportedError(
                        title="`$content` field for node of type",
                        value=_type
                    )
                return None
            case _:
                never(_type)

    def _convert_nodes(
        self,
        node: FileTreeNode
    ) -> dict[str, FileTreeNodeInternal] | None:
        if node.root is None:
            return None

        result: dict[str, FileTreeNodeInternal] = {}
        for k, v in node.root.items():
            if isinstance(v, FileTreeNode):
                result[k] = self.convert(v)

        return result
