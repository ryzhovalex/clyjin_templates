from pathlib import Path
from clyjin.base import Module, ModuleArg
from clyjin.log import Log
from clyjin.base import Config
from mako.template import Template

from clyjin_templates.args import TemplatesArgs


class RootModule(Module[TemplatesArgs, Config]):
    NAME = "_root"
    DESCRIPTION = "create files and directories using templates"
    ARGS = TemplatesArgs(
        template=ModuleArg[str](
            names=["template"],
            type=str,
            help="which template to use"
        )
    )

    async def execute(self) -> None:
        template_name: str = self.args.template.value
        Log.info(
            f"[clyjin_templates] chosen template <{template_name}>"
        )

        t = Template(filename=str(Path(self._rootdir, "tests", "test.py.mako")))
        Log.debug(t.render(x=2, y=3))
