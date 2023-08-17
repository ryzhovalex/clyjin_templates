from pydantic import RootModel
from clyjin_templates.template.vars.var import TemplateGroupVar


class TemplateGroupVars(RootModel):
    root: dict[str, TemplateGroupVar | None]
