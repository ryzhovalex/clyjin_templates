from enum import Enum
from pathlib import Path
from typing import TYPE_CHECKING
from clyjin_templates.template.refname import RefTemplateName

if TYPE_CHECKING:
    from clyjin_templates.filetree.node import FileTreeNode


class NodeFieldKey(Enum):
    """
    Various key fields used to build File Tree structures.

    All should be prefixed by dollar sign.

    Attributes:
        Type:
            Type of a node.
        Content:
            Content of a file.
    """
    Type = "$type"
    Content = "$content"


class NodeType(Enum):
    File = "file"
    Dir = "dir"


NodeContent = Path | str | RefTemplateName
NodeFieldValue = FileTreeNode | NodeType | NodeContent
NodeRoot = dict[str, NodeFieldValue | None]
