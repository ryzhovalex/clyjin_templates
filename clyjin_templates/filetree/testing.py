from pathlib import Path
import pytest

from clyjin_templates.filetree.node import FileTreeNode, FileTreeNodeInternal
from clyjin_templates.filetree.nodeconverter import InternalFileTreeNodeConverter
from clyjin_templates.template.group import TemplateGroup


@pytest.fixture
def s1_root_node(s1_templategroup: TemplateGroup) -> FileTreeNode:
    return s1_templategroup.tree


@pytest.fixture
def s1_root_node_internal(s1_root_node: FileTreeNode) -> FileTreeNodeInternal:
    return InternalFileTreeNodeConverter().convert(s1_root_node)
