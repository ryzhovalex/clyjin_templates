from pathlib import Path
from typing import TYPE_CHECKING

from clyjin.log import Log

if TYPE_CHECKING:
    from clyjin_templates.filesystem.models import FileTreeNodeInternal
    from clyjin_templates.template.group import TemplateGroup


class FileMaker:
    """
    Makes files and directories out of templates.
    """
    def __init__(self) -> None:
        pass

    async def make(
        self,
        template_group: "TemplateGroup",
        target_dir: Path,
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
        Log.info(
            "[clyjin_templates.filesystem] making file tree for"
            f" template <{template_group.name}>"
            f" in dir <{target_dir}>",
        )

    async def _make_node(
        self,
        node: "FileTreeNodeInternal",
    ) -> None:
        pass
