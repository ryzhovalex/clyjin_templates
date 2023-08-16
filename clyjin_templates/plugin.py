from clyjin.base import Plugin
from clyjin_templates.rootmodule import RootModule
from clyjin_templates._project import get_version


class TemplatesPlugin(Plugin):
    NAME = "template"
    MODULE_CLASSES = [
        RootModule
    ]
    VERSION = get_version()
