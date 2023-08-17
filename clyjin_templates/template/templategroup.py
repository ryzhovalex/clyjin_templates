from clyjin.base import Model
from clyjin_templates.template.filetree.node import FileTreeNode
from clyjin_templates.template.vars.vars import TemplateGroupVars

from clyjin_templates.template.template import Template


class TemplateGroup(Model):
    """
    Collection of templates executed at once to form a directory structure.

    Attributes:
        name:
            Name of a group.
        tree:
            File tree structure for a group.
        templates(optional):
            Templates attached to a group. Named without `.mako` suffix.
            Defaults to None.
        description(optional):
            Description text of a group. Defaults to None.
        vars(optional):
            Variables context of this group. Defaults to None.
    """
    name: str
    tree: FileTreeNode
    templates: dict[str, Template]
    description: str | None = None
    vars: TemplateGroupVars | None = None
