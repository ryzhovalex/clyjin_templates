from pathlib import Path
from clyjin.base import Plugin, Module, PluginInitializeData

from clyjin_templates._project import get_version
from clyjin_templates.boot import Boot
from clyjin_templates.rootmodule import RootModule
from clyjin_templates.template.group_service import TemplateGroupService
from clyjin_templates.utils.servicehub import ServiceHub


class TemplatesPlugin(Plugin):
    NAME = "template"
    MODULE_CLASSES = [
        RootModule,
    ]
    VERSION = get_version()

    @classmethod
    async def initialize(
        cls,
        data: PluginInitializeData
    ) -> None:
        await Boot(data).start()

        service_hub: ServiceHub = ServiceHub.ie()

        template_group_service: TemplateGroupService = service_hub.get(
            TemplateGroupService
        )
        await template_group_service.load()
