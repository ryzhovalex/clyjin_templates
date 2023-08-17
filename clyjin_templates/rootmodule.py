from pathlib import Path

from clyjin.base import Config, Module, ModuleArg
from clyjin.base.moduledata import ModuleData
from clyjin.log import Log

from clyjin_templates.args import TemplatesArgs
from clyjin_templates.template.group_service import TemplateGroupService
from clyjin_templates.template.templategroup import TemplateGroup
from clyjin_templates.utils.servicehub import ServiceHub


class RootModule(Module[TemplatesArgs, Config]):
    NAME = "_root"
    DESCRIPTION = "create files and directories using templates"
    ARGS = TemplatesArgs(
        template_group=ModuleArg[str](
            names=["template_group"],
            type=str,
            help="which template group to use",
        ),
    )

    def __init__(
        self,
        module_data: ModuleData[TemplatesArgs, Config]
    ) -> None:
        super().__init__(module_data)

        self._template_group_service: TemplateGroupService = \
            ServiceHub.ie().get(TemplateGroupService)

    async def execute(self) -> None:
        template_group_name: str = self.args.template_group.value
        Log.info(
            "[clyjin_templates] choosing template"
            f" group <{template_group_name}>"
        )

        template_group: TemplateGroup = self._template_group_service.get(
            template_group_name
        )
