from pathlib import Path

from clyjin.base import Config, Module, ModuleArg
from clyjin.base.moduledata import ModuleData
from clyjin.log import Log
from antievil import UnsetValueError

from clyjin_templates.args import TemplatesArgs
from clyjin_templates.template.filemaker.maker import FileMaker
from clyjin_templates.template.group_service import TemplateGroupService
from clyjin_templates.template.group import TemplateGroup
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
        target_dir=ModuleArg[Path](
            names=["-o", "--output-dir"],
            type=Path,
            required=False,
            help="where to output generated files. Defaults to current dir."
        )
    )

    def __init__(
        self,
        module_data: ModuleData[TemplatesArgs, Config]
    ) -> None:
        super().__init__(module_data)

        self._template_group_service: TemplateGroupService

    async def execute(self) -> None:
        self._initialize()

        template_group_name: str = self.args.template_group.value
        target_dir: Path = self._get_target_dir()

        Log.info(
            "[clyjin_templates] choosing template"
            f" group <{template_group_name}>"
        )

        template_group: TemplateGroup = self._template_group_service.get(
            template_group_name
        )

        await FileMaker().make(template_group, target_dir)

    def _initialize(self) -> None:
        self._template_group_service = ServiceHub.ie().get(
            TemplateGroupService
        )

    def _get_target_dir(self) -> Path:
        try:
            return self.args.target_dir.value
        except UnsetValueError:
            return self._rootdir
