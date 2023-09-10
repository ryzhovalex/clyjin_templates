from pathlib import Path
from typing import TYPE_CHECKING

from antievil import DirectoryExpectError, UnsetValueError
from clyjin.base import Config, Module, ModuleArg
from clyjin.base.moduledata import ModuleData
from clyjin.log import Log

from clyjin_templates.args import AddArgs, TemplatesArgs
from clyjin_templates.filesystem.maker import FileNodeMaker
from clyjin_templates.template.group_service import TemplateGroupService
from clyjin_templates.utils.servicehub import ServiceHub

if TYPE_CHECKING:
    from clyjin_templates.template.group import TemplateGroup


class RootModule(Module[TemplatesArgs, Config]):
    Name = "$root"
    Description = "creates files and directories using template group"
    Args = TemplatesArgs(
        template_group=ModuleArg[str](
            names=["template_group"],
            type=str,
            help="which template group to use",
        ),
        target_dir=ModuleArg[Path](
            names=["-o", "--output-dir"],
            type=Path,
            required=False,
            help="where to output generated files. Defaults to current dir.",
        ),
    )

    def __init__(
        self,
        module_data: ModuleData[TemplatesArgs, Config],
    ) -> None:
        super().__init__(module_data)

        self._template_group_service: TemplateGroupService

    async def execute(self) -> None:
        self._initialize()

        template_group_name: str = self.args.template_group.value
        target_dir: Path = self._get_target_dir()
        if target_dir.exists() and not target_dir.is_dir():
            raise DirectoryExpectError(
                path=target_dir,
            )
        target_dir.mkdir(parents=True, exist_ok=True)

        Log.info(
            "[clyjin_templates] choosing template"
            f" group <{template_group_name}>",
        )

        template_group: TemplateGroup = self._template_group_service.get(
            template_group_name,
        )

        await FileNodeMaker().make(template_group, target_dir)

    def _initialize(self) -> None:
        self._template_group_service = ServiceHub.ie().get(
            TemplateGroupService,
        )

    def _get_target_dir(self) -> Path:
        try:
            return self.args.target_dir.value
        except UnsetValueError:
            return self._rootdir


class RegisterModule(Module[AddArgs, Config]):
    Name = "register"
    Description = "registers a new template"
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
                " Dir's name is used by default.",
        ),
        is_update=ModuleArg[bool](
            names=["-u", "--update"],
            action="store_true",
            type=bool,
            argparse_type=type,
            help=
                "if should overwrite existing group."
                " By default will raise an error if an existing group occurs.",
        ),
    )

    def __init__(
        self,
        module_data: ModuleData[AddArgs, Config],
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
            is_update=self.args.is_update,
        )

    def _initialize(self) -> None:
        self._template_group_service = ServiceHub.ie().get(
            TemplateGroupService,
        )

    def _get_name(self) -> str | None:
        try:
            return self.args.template_group_name.value
        except UnsetValueError:
            return None
