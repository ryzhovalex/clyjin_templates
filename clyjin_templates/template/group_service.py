import os
import aiofiles
from pathlib import Path

from antievil import NotFoundError

from clyjin_templates.template.templategroup import TemplateGroup
from clyjin_templates.utils.service import Service


class TemplateGroupService(Service):
    """
    Manages Template Groups.
    """
    def __init__(
        self,
        root_dir: Path,
        groups_dir: Path
    ) -> None:
        self._root_dir: Path = root_dir
        self._groups_dir: Path = groups_dir
        self._is_loaded: bool = False
        self._group_by_name: dict[str, TemplateGroup] = {}

    def get(self, name: str) -> TemplateGroup:
        """
        Gets group by name.
        """
        try:
            return self._group_by_name[name]
        except KeyError as error:
            raise NotFoundError(
                title="template group with name",
                value=name
            ) from error

    async def load(self) -> None:
        """
        Loads saved groups into memory.
        """
        # for root, dirnames, _ in os.walk(self._groups_dir):
        for root, dirnames, _ in os.walk(Path(self._root_dir, )):
            print(dirnames)
