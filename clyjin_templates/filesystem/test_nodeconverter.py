from clyjin_templates.filesystem.models import (FileTreeNode,
                                                FileTreeNodeInternal, NodeRoot, NodeType)
from clyjin_templates.filesystem.nodeconverter import \
    FileTreeNodeConverter
from clyjin_templates.template.group import TemplateGroup


def test_s1(s1_root_node_internal: FileTreeNodeInternal):
    node: FileTreeNodeInternal = s1_root_node_internal

    expected_node: FileTreeNodeInternal = FileTreeNodeInternal(
        type=NodeType.Dir,
        content=None,
        nodes={
            "src": FileTreeNodeInternal(
                type=NodeType.Dir,
                content=None,
                nodes={
                    "__init__.py": FileTreeNodeInternal(
                        type=NodeType.File,
                        content="&s1_1.py",
                        nodes=None
                    ),
                    "drivers": FileTreeNodeInternal(
                        type=NodeType.Dir,
                        content=None,
                        nodes={
                            "main.py": FileTreeNodeInternal(
                                type=NodeType.File,
                                content="&s1_2.py",
                                nodes=None
                            )
                        }
                    ),
                    "local": FileTreeNodeInternal(
                        type=NodeType.Dir,
                        content=None,
                        nodes=None
                    )
                }
            ),
            "README.md": FileTreeNodeInternal(
                type=NodeType.File,
                content="# s1_readme"
            )
        }
    )

    assert node == expected_node
