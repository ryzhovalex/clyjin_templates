from clyjin_templates.template.group_service import TemplateGroupService
from clyjin_templates.utils.service import Service
from clyjin_templates.utils.servicehub import ServiceHub


class Boot:
    _SERVICE_CLASSES: list[type[Service]] = [
        TemplateGroupService
    ]

    @classmethod
    async def start(cls) -> None:
        services: list[Service] = []

        for ServiceClass in cls._SERVICE_CLASSES:
            services.append(ServiceClass())

        ServiceHub(services)
