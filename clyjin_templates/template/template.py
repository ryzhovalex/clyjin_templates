from pathlib import Path
from clyjin.base import Model

from clyjin_templates.template.templatesource import TemplateSource
from clyjin_templates.template.vars.scope import TemplateGroupVarScope, TemplateGroupVarSpecialScope

RefTemplateName = str
"""
Reference variant of template name, prefixed with ampersand `&`.
"""


class Template(Model):
    """
    Basic unit to be parsed.

    Attributes:
        source(optional):
            Source to fetch a template. Defaults to path to template file
            in the directory of the group spec. The file should have extension
            `.mako` and the same name as provided as a template name in the
            spec.
        scope(optional):
            Variable scope this template works in. Defaults to `$all`.
    """
    source: TemplateSource | None = None
    scope: TemplateGroupVarScope = TemplateGroupVarSpecialScope.All
