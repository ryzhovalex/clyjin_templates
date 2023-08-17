import importlib.metadata
from clyjin_templates._project import get_version as _get_version
from clyjin_templates.plugin import TemplatesPlugin

__version__ = importlib.metadata.version("clyjin_templates")
MainPlugin = TemplatesPlugin
