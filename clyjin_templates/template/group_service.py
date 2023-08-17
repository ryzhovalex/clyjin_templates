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
        groups_dir: Path
    ) -> None:
        self._groups_dir: Path = groups_dir
        self._is_loaded: bool = False
        self._group_by_name: dict[str, TemplateGroup] = {}

    async def get(self, name: str) -> TemplateGroup:
        """
        Gets group by name.
        """
        await self._lazyload()

        try:
            return self._group_by_name[name]
        except KeyError as error:
            raise NotFoundError(
                title="template group with name",
                value=name
            ) from error

    async def _lazyload(self) -> None:
        """
        Loads groups if not have been done.
        """
        if self._is_loaded:
            return



        self._is_loaded = True
