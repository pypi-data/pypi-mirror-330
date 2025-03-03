from pytopvisor.services.projects import ProjectsService
from pytopvisor.services.positions import PositionsService


class ServiceFactory:
    def __init__(self, api_client):
        self.api_client = api_client
        self._services = {}

    def get_service(self, service_name):

        if service_name not in self._services:

            if service_name == "projects":
                self._services[service_name] = ProjectsService(self.api_client)
            elif service_name == "positions":
                self._services[service_name] = PositionsService(self.api_client)
            else:
                raise ValueError(f"Unknown service: {service_name}")
        return self._services[service_name]

