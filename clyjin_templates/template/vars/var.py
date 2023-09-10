from clyjin.base import Model

from clyjin_templates.template.vars.scope import (
    TemplateGroupVarScope,
    TemplateGroupVarSpecialScope,
)

TemplateGroupVarValue = str | int | float | bool | list | dict


class TemplateGroupVar(Model):
    """
    Variable in the template's context.

    Attributes:
        default(optional):
            Default value set to a variable if no value is given on input.
            Defaults to required value, i.e. it will be mandatory to define
            the variable on input.
        scope(optional):
            Scope of a variable.
    """
    default: TemplateGroupVarValue | None = None
    scopes: TemplateGroupVarScope = TemplateGroupVarSpecialScope.All
