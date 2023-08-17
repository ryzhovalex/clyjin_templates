from clyjin_templates.utils.service import Service
from clyjin_templates.utils.singleton import Singleton
from antievil import NotFoundError


class ServiceHub(Singleton):
    """
    Stores all services.
    """
    def __init__(
        self,
        services: list[Service]
    ) -> None:
        super().__init__()

        self._service_by_name: dict[str, Service] = {}

        self._initialize_services(services)

    def get(self, name: str) -> Service:
        try:
            return self._service_by_name[name]
        except KeyError as error:
            raise NotFoundError(
                title="service with name",
                value=name
            ) from error

    def _initialize_services(self, services: list[Service]) -> None:
        for service in services:
            self._service_by_name[service.__class__.__name__] = service
