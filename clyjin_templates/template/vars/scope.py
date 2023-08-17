from enum import Enum


class TemplateGroupVarSpecialScope(Enum):
    """
    Special keywords for var scopes.

    Attributes:
        All:
            All templates will have this var context.
    """
    All = "$all"


TemplateGroupCustomScope = str
TemplateGroupVarScope = \
    TemplateGroupVarSpecialScope | TemplateGroupCustomScope
