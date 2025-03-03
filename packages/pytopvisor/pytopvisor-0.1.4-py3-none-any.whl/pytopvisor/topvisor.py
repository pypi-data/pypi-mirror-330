from pytopvisor.services.api import TopvisorAPI
from pytopvisor.services.factory import ServiceFactory


class Topvisor:
    def __init__(self, user_id, api_key):
        self.api_client = TopvisorAPI(user_id, api_key)
        self.service_factory = ServiceFactory(self.api_client)

    def get_operation_mapping(self):
        """
        Returns a dictionary mapping operations.
        Key: operation name.
        Value: tuple (service, method).
        """
        return {
            "get_projects": ("projects", "get_projects"),
            "get_competitors": ("projects", "get_competitors"),
            "get_history": ("positions", "get_history"),
            "get_summary": ("positions", "get_summary"),
            "get_summary_chart": ("positions", "get_summary_chart"),
            "get_searchers_regions": ("positions", "get_searchers_regions"),
        }

    def run_task(self, task_name, **kwargs):
        """
        Universal method for executing operations.

        :param task_name: Operation name.
        :param kwargs: Arguments for the operation.
        :return: Operation execution result.
        """

        operation_mapping = self.get_operation_mapping()

        if task_name not in operation_mapping:
            raise ValueError(f"Unknown operation: {task_name}")

        service_name, method_name = operation_mapping[task_name]
        service = self.service_factory.get_service(service_name)

        method = getattr(service, method_name, None)

        if not method:
            raise AttributeError(
                f"Method {method_name} not found in service {service_name}"
            )

        return method(**kwargs)