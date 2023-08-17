from clyjin_templates.filetree.node import FileTreeNode
from pathlib import Path
from antievil import ExpectedTypeError, PleaseDefineError, UnsupportedError
from clyjin.log import Log
from mako.template import Template as MakoTemplate
from clyjin_templates.filetree.node import FileTreeNode, FileTreeNodeInternal
from clyjin_templates.filetree.types import NodeContent, NodeFieldValue, NodeRoot, NodeType
from clyjin_templates.template.group import TemplateGroup
from clyjin_templates.template.refname import RefTemplateName


class InternalFileTreeNodeConverter:
    """
    Converts external FileTreeNodes to internal variants.
    """
    def convert(
        self,
        external_node: FileTreeNode
    ) -> FileTreeNodeInternal:

        noderoot: NodeRoot | None = external_node.root
        nodetype: NodeType = self._get_node_type(noderoot)

        nodecontent: NodeContent | None = None
        if noderoot is not None:
            nodecontent = self._get_node_content(
                noderoot,
                nodetype
            )

        return FileTreeNodeInternal(
            type=nodetype,
            content=nodecontent,
            nodes=
        )

    def _get_node_type(
        self,
        noderoot: NodeRoot | None
    ) -> NodeType:
        if noderoot is None:
            return NodeType.Dir

        nodetype: NodeFieldValue | None = noderoot["$type"]

        if nodetype is None:
            return NodeType.File
        elif not isinstance(nodetype, NodeType):
            raise ExpectedTypeError(
                obj=nodetype,
                ExpectedType=NodeType,
                is_instance_expected=True,
                ActualType=type(nodetype)
            )
        return nodetype

    def _get_node_content(
        self,
        noderoot: NodeRoot,
        nodetype: NodeType
    ) -> NodeContent | None:
        nodecontent: NodeFieldValue | None = noderoot["$content"]

        if nodetype is NodeType.File:
            if nodecontent is None:
                raise PleaseDefineError(
                    cannot_do="file-type node initializing",
                    please_define="`$content` field"
                )
            elif not isinstance(nodecontent, str):
                raise ExpectedTypeError(
                    obj=nodecontent,
                    ExpectedType=str,
                    is_instance_expected=True,
                    ActualType=type(nodecontent)
                )

            # check if it is Path
        elif nodetype is NodeType.Dir:
            if nodecontent is not None:
                raise UnsupportedError(
                    title="`$content` field for node of type",
                    value=nodetype
                )
            return None
