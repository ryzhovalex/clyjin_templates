from pathlib import Path

from clyjin.base import Config, Module, ModuleArg
from clyjin.base.moduledata import ModuleData
from clyjin.log import Log
from mako.template import Template

from clyjin_templates.args import TemplatesArgs


class RootModule(Module[TemplatesArgs, Config]):
    NAME = "_root"
    DESCRIPTION = "create files and directories using templates"
    ARGS = TemplatesArgs(
        template=ModuleArg[str](
            names=["template"],
            type=str,
            help="which template to use",
        ),
    )

    def __init__(
        self,
        module_data: ModuleData[TemplatesArgs, Config]
    ) -> None:
        super().__init__(module_data)

        self._groups

    async def execute(self) -> None:
        template_name: str = self.args.template.value
        Log.info(
            f"[clyjin_templates] chosen template <{template_name}>",
        )

        t = Template(
            filename=str(Path(self._rootdir, "tests", "test.py.mako")),
        )
        Log.debug(self._plugin_common_sysdir)
