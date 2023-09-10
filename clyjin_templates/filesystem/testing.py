import pytest

from clyjin_templates.filesystem.models import (FileTreeNode,
                                                FileTreeNodeInternal)
from clyjin_templates.filesystem.nodeconverter import \
    FileTreeNodeConverter
from clyjin_templates.template.group import TemplateGroup


@pytest.fixture
def s1_root_node(s1_templategroup: TemplateGroup) -> FileTreeNode:
    return s1_templategroup.tree


@pytest.fixture
def s1_root_node_internal(s1_root_node: FileTreeNode) -> FileTreeNodeInternal:
    return FileTreeNodeConverter().convert(s1_root_node)
