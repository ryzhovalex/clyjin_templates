import os
import shutil
import aiofiles
from pathlib import Path

from antievil import NotFoundError
from clyjin.log import Log
from clyjin_templates.template.errors import IncorrectTemplateGroupNameError

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

    async def add(
        self,
        dir: Path,
        name: str | None = None
    ) -> None:
        """
        Adds a new template group to the storage.

        The name for template group will be taken according to the passed
        directory's name, unless `name` is specified.

        Args:
            template_group_dir:
                Directory where a template group resides. The dir should
                contain at least `spec.yml` file at the root level.
        """
        self._softcheck_group_dir(dir)
        final_name: str = \
            dir.name if name is None else name
        self._check_name(final_name)

        Log.info(
            f"[clyjin_templates] adding template <{final_name}>"
            f" group from path <{dir}>"
        )

        destination_dir: Path = Path(
            self._groups_dir,
            final_name
        )

        Log.info(
            f"[clyjin_templates] copying group <{final_name}>"
            f" from <{dir}> to <{destination_dir}>"
        )

        # do regular 1-to-1 copying
        shutil.copy(
            dir,
            destination_dir
        )

        await self._load(final_name)

    def _check_name(self, name: str) -> None:
        """
        Checks group name for correctness.
        """
        if name == "":
            raise IncorrectTemplateGroupNameError(name, "empty")
        elif not name.isalnum():
            raise IncorrectTemplateGroupNameError(name, "not alpha-numeric")

    def _softcheck_group_dir(self, group_dir: Path) -> None:
        """
        Checks that a group dir should contain at least `spec.yml` file.

        Other checks, such as proper structure of `spec.yml` will be done only
        at the first template call.

        Maybe in future the initial check will be performed outputting the
        template to some temporary directory for test purposes.
        """
        if not Path(group_dir, "spec.yml").is_file():
            raise NotFoundError(
                title="spec file for template group dir",
                value=group_dir
            )

    async def preload(self) -> None:
        """
        Loads saved groups into memory.
        """
        # for root, dirnames, _ in os.walk(self._groups_dir):
        for root, dirnames, _ in os.walk(
            Path(self._root_dir, self._groups_dir)
        ):
            print(dirnames)

    async def _load(self, name: str) -> None:
        """
        Loads template groups from storage into main memory.
        """
