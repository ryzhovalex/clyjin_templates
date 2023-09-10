import importlib.metadata
from clyjin.base import Plugin, PluginInitializeData

from clyjin_templates.add_module import AddModule
from clyjin_templates.boot import Boot
from clyjin_templates.root_module import RootModule
from clyjin_templates.template.group_service import TemplateGroupService
from clyjin_templates.utils.servicehub import ServiceHub


class TemplatesPlugin(Plugin):
    Name = "template"
    ModuleClasses = [
        RootModule,
        AddModule
    ]
    Version = importlib.metadata.version("clyjin_templates")

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
        await template_group_service.preload()
