from enum import Enum


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
