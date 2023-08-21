from pathlib import Path
from clyjin.base import Model
from pydantic import Field, RootModel
from clyjin_templates.filetree.types import NodeContent, NodeFieldValue, NodeRoot, NodeType


class FileTreeNode(RootModel):
    """
    Describes filetree structure of a template group.

    Attributes:
        $type(optional):
            Type of a node. Defaults to file type if no subnodes are available,
            otherwise defaults to dir type. Usually requires to be set
            explicitly if a user wants to create an empty directory (to avoid
            treating it as an empty file).
        $content(optional):
            Content of a node. For dir types should equal to None. Defaults
            to None. For files None would mean that no content will be written,
            but a new file will be created. Can be set to reference template
            name, by prefixing needed template name with an ampersand `&`.
        ...nodes(optional):
            Children nodes by names. Should be None for file types. Defaults
            to None. Are accessed under other arbitrary names.
    """
    root: NodeRoot | None = None


class FileTreeNodeInternal(Model):
    """
    Parsed internal version of
    ${ref.clyjin_templates.filetree.node.FileTreeNode}.
    """
    type: NodeType
    content: NodeContent | None = None
    nodes: dict[str, "FileTreeNodeInternal"] | None = None
