from pathlib import Path
from clyjin.base.moduleargs import ModuleArg, ModuleArgs


class TemplatesArgs(ModuleArgs):
    template_group: ModuleArg[str]
    target_dir: ModuleArg[Path]


class AddArgs(ModuleArgs):
    template_group_dir: ModuleArg[Path]
    template_group_name: ModuleArg[str]
    is_update: ModuleArg[bool]
