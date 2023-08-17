from pathlib import Path
from clyjin_templates.template.group import TemplateGroup


class FileMaker:
    """
    Makes files and directories out of templates.
    """
    def __init__(self) -> None:
        pass

    async def make(
        self,
        template_group: TemplateGroup,
        target_dir: Path
    ) -> None:
        """
        Executes template group saving according files and directories to
        chosen dir.

        Args:
            template_group:
                Group to execute.
            target_dir:
                Where to save generated files and directories.
        """
