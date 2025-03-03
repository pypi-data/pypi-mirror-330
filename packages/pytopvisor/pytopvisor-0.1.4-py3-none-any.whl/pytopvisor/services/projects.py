from .base import BaseService
from pytopvisor.utils.payload import PayloadFactory
from typing import Optional


class ProjectsService(BaseService):
    def __init__(self, api_client):
        super().__init__(api_client)
        self.endpoints = {
            "projects": "/v2/json/get/projects_2/projects",
            "competitors": "/v2/json/get/projects_2/competitors",
        }

    def get_projects(
        self,
        show_site_stat: Optional[bool] = None,
        show_searchers_and_regions: Optional[int] = None,
        include_positions_summary: Optional[bool] = None,
    ):
        """
        Retrieves a list of projects.
        """
        payload = PayloadFactory.projects_get_projects_payload(
            show_site_stat=show_site_stat,
            show_searchers_and_regions=show_searchers_and_regions,
            include_positions_summary=include_positions_summary,
        )

        return self.send_request(self.endpoints["projects"], payload)

    def get_competitors(
        self,
        project_id: int,
        only_enabled: Optional[bool] = None,
        include_project: Optional[bool] = None,
    ):
        """
        Retrieves a list of competitors.
        """
        payload = PayloadFactory.projects_get_competitors_payload(
            project_id=project_id,
            only_enabled=only_enabled,
            include_project=include_project,
        )

        return self.send_request(self.endpoints["competitors"], payload)

