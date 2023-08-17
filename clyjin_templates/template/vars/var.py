from clyjin.base import Model
from clyjin_templates.template.vars.scope import TemplateGroupVarScope, TemplateGroupVarSpecialScope

TemplateGroupVarValue = str | int | float | bool | list | dict


class TemplateGroupVar(Model):
    """
    Variable in the template's context.

    Attributes:
        value:
            Value set to a variable.
        scope(optional):
            Scope of a variable.
    """
    value: TemplateGroupVarValue
    scopes: TemplateGroupVarScope = TemplateGroupVarSpecialScope.All
