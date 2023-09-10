from pathlib import Path

from clyjin.base import Config, Module, ModuleArg
from clyjin.base.moduledata import ModuleData
from antievil import UnsetValueError
from clyjin.log import Log

from clyjin_templates.args import AddArgs, TemplatesArgs
from clyjin_templates.template.group_service import TemplateGroupService
from clyjin_templates.template.group import TemplateGroup
from clyjin_templates.utils.servicehub import ServiceHub


class AddModule(Module[AddArgs, Config]):
    Name = "add"
    Description = "create files and directories using templates"
    Args = AddArgs(
        template_group_dir=ModuleArg[Path](
            names=["template_group_dir"],
            type=Path,
            help="from which dir to add new template group",
        ),
        template_group_name=ModuleArg[str](
            names=["--name"],
            type=str,
            help=
                "name to assign for added template group."
                " Dir's name is used by default."
        ),
        is_update=ModuleArg[bool](
            names=["-u", "--update"],
            action="store_true",
            type=bool,
            argparse_type=type,
            help=
                "if should overwrite existing group."
                " By default will raise an error if an existing group occurs."
        )
    )

    def __init__(
        self,
        module_data: ModuleData[AddArgs, Config]
    ) -> None:
        super().__init__(module_data)

        self._template_group_service: TemplateGroupService

    async def execute(self) -> None:
        self._initialize()
        input_dir: Path = self.args.template_group_dir.value
        name: str | None = self._get_name()
        await self._template_group_service.add(
            input_dir,
            name=name,
            is_update=self.args.is_update
        )

    def _initialize(self) -> None:
        self._template_group_service = ServiceHub.ie().get(
            TemplateGroupService
        )

    def _get_name(self) -> str | None:
        try:
            return self.args.template_group_name.value
        except UnsetValueError:
            return None
