from pathlib import Path

from clyjin_templates.plugin import TemplatesPlugin
from clyjin_templates._project import get_version as _get_version

__version__ = _get_version()
MainPlugin = TemplatesPlugin
