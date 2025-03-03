from .base import BaseService
from pytopvisor.utils.payload import PayloadFactory
from typing import List, Optional


class PositionsService(BaseService):

    def __init__(self, api_client):
        super().__init__(api_client)
        self.endpoints = {
            "history": "/v2/json/get/positions_2/history",
            "summary": "/v2/json/get/positions_2/summary",
            "summary_chart": "/v2/json/get/positions_2/summary/chart",
            "checker_price": "/v2/json/get/positions_2/checker/price",
            "searchers_regions_export": "/v2/json/get/positions_2/searchers/regions/export",
        }

    def get_history(
        self,
        project_id: int,
        regions_indexes: List[int],
        dates: Optional[List[str]] = None,
        date1: Optional[str] = None,
        date2: Optional[str] = None,
        competitors_ids: Optional[List[int]] = None,
        type_range: Optional[int] = None,
        count_dates: Optional[int] = None,
        only_exists_first_date: Optional[bool] = None,
        show_headers: Optional[bool] = None,
        show_exists_dates: Optional[bool] = None,
        show_visitors: Optional[bool] = None,
        show_top_by_depth: Optional[int] = None,
        positions_fields: Optional[List[str]] = None,
        filter_by_dynamic: Optional[List[str]] = None,
        filter_by_positions: Optional[List[List[int]]] = None,
    ):
        """
        Retrieves the history of position checks.
        :param project_id: Project ID (required).
        :param regions_indexes: List of region indexes (required).
        :param dates: List of arbitrary check dates (in YYYY-MM-DD format).
        :param date1: Start date of the period (in YYYY-MM-DD format).
        :param date2: End date of the period (in YYYY-MM-DD format).
        :param competitors_ids: List of competitor IDs.
        :param type_range: Date range (enum: 0-7, 100).
        :param count_dates: Maximum number of returned dates (no more than 31).
        :param only_exists_first_date: Display only keywords present in the first check.
        :param show_headers: Add result headers.
        :param show_exists_dates: Add check dates.
        :param show_visitors: Add visitor data.
        :param show_top_by_depth: Add data for the specified depth of the TOP.
        :param positions_fields: Select columns of data with check results.
        :param filter_by_dynamic: Filter by keyword dynamics.
        :param filter_by_positions: Filter by keyword positions.
        :return: Request result.
        """
        # Validate required parameters
        if not isinstance(project_id, int):
            raise ValueError("project_id must be an integer.")
        if not isinstance(regions_indexes, list) or not all(
            isinstance(idx, int) for idx in regions_indexes
        ):
            raise ValueError("regions_indexes must be a list of integers.")

        # Validate dates
        if dates and (date1 or date2):
            raise ValueError("Cannot pass both 'dates' and 'date1/date2'.")
        if (date1 and not date2) or (date2 and not date1):
            raise ValueError("Both 'date1' and 'date2' must be specified.")
        if dates and not all(
            isinstance(date, str) and len(date) == 10 for date in dates
        ):
            raise ValueError(
                "All elements in 'dates' must be strings in YYYY-MM-DD format."
            )
        if date1 and not isinstance(date1, str) or date2 and not isinstance(date2, str):
            raise ValueError(
                "Parameters 'date1' and 'date2' must be strings in YYYY-MM-DD format."
            )

        # Формирование payload
        try:
            payload = PayloadFactory.positions_get_history_payload(
                project_id=project_id,
                regions_indexes=regions_indexes,
                dates=dates,
                date1=date1,
                date2=date2,
                competitors_ids=competitors_ids,
                type_range=type_range,
                count_dates=count_dates,
                only_exists_first_date=only_exists_first_date,
                show_headers=show_headers,
                show_exists_dates=show_exists_dates,
                show_visitors=show_visitors,
                show_top_by_depth=show_top_by_depth,
                positions_fields=positions_fields,
                filter_by_dynamic=filter_by_dynamic,
                filter_by_positions=filter_by_positions,
            )
        except Exception as e:
            raise RuntimeError(f"Error while forming payload: {e}")

        return self.send_request(self.endpoints["history"], payload)

    def get_summary(
        self,
        project_id: int,
        region_index: int,
        dates: List[str],
        competitor_id: Optional[int] = None,
        only_exists_first_date: Optional[bool] = None,
        show_dynamics: Optional[bool] = None,
        show_tops: Optional[bool] = None,
        show_avg: Optional[bool] = None,
        show_visibility: Optional[bool] = None,
        show_median: Optional[bool] = None,
    ):
        """
        Retrieves summary data for the selected project over two dates.
        :param project_id: Project ID.
        :param region_index: Region index.
        :param dates: List of two dates for building the summary.
        :param competitor_id: Competitor ID (optional).
        :param only_exists_first_date: Consider keywords present in both dates (boolean).
        :param show_dynamics: Add position dynamics (boolean).
        :param show_tops: Add TOP data (boolean).
        :param show_avg: Add average position (boolean).
        :param show_visibility: Add visibility (boolean).
        :param show_median: Add median position (boolean).
        :return: Request result.
        """
        # Validate required parameters
        if not isinstance(project_id, int):
            raise ValueError("project_id must be an integer.")
        if not isinstance(region_index, int):
            raise ValueError("region_index must be an integer.")
        if not isinstance(dates, list) or len(dates) != 2:
            raise ValueError("dates must be a list of two dates.")
        if not all(isinstance(date, str) and len(date) == 10 for date in dates):
            raise ValueError(
                "All elements in 'dates' must be strings in YYYY-MM-DD format."
            )


        try:
            payload = PayloadFactory.positions_get_summary_payload(
                project_id=project_id,
                region_index=region_index,
                dates=dates,
                competitor_id=competitor_id,
                only_exists_first_date=only_exists_first_date,
                show_dynamics=show_dynamics,
                show_tops=show_tops,
                show_avg=show_avg,
                show_visibility=show_visibility,
                show_median=show_median,
            )
        except Exception as e:
            raise RuntimeError(f"Error while forming payload: {e}")

        return self.send_request(self.endpoints["summary"], payload)

    def get_summary_chart(
        self,
        project_id: int,
        region_index: int,
        dates: Optional[List[str]] = None,
        date1: Optional[str] = None,
        date2: Optional[str] = None,
        competitors_ids: Optional[List[int]] = None,
        type_range: Optional[int] = None,
        only_exists_first_date: Optional[bool] = None,
        show_tops: Optional[bool] = None,
        show_avg: Optional[bool] = None,
        show_visibility: Optional[bool] = None,
    ):
        """
        Retrieves data for the summary chart for the selected project.
        :param project_id: Project ID.
        :param region_index: Region index.
        :param dates: List of arbitrary check dates.
        :param date1: Start date of the period.
        :param date2: End date of the period.
        :param competitors_ids: List of competitor IDs (or project ID).
        :param type_range: Date range (enum: 0, 1, 2, 3, 4, 5, 6, 7, 100).
        :param only_exists_first_date: Consider keywords present in all dates (boolean).
        :param show_tops: Add TOP data (boolean).
        :param show_avg: Add average position (boolean).
        :param show_visibility: Add visibility (boolean).
        :return: Request result.
        """
        # Validate required parameters
        if not isinstance(project_id, int):
            raise ValueError("project_id must be an integer.")
        if not isinstance(region_index, int):
            raise ValueError("region_index must be an integer.")
        if dates and (date1 or date2):
            raise ValueError("Cannot pass both 'dates' and 'date1/date2'.")
        if (date1 and not date2) or (date2 and not date1):
            raise ValueError("Both 'date1' and 'date2' must be specified.")
        if dates and not all(
            isinstance(date, str) and len(date) == 10 for date in dates
        ):
            raise ValueError(
                "All elements in 'dates' must be strings in YYYY-MM-DD format."
            )
        if date1 and not isinstance(date1, str) or date2 and not isinstance(date2, str):
            raise ValueError(
                "Parameters 'date1' and 'date2' must be strings in YYYY-MM-DD format."
            )

        try:
            payload = PayloadFactory.positions_get_summary_chart_payload(
                project_id=project_id,
                region_index=region_index,
                dates=dates,
                date1=date1,
                date2=date2,
                competitors_ids=competitors_ids,
                type_range=type_range,
                only_exists_first_date=only_exists_first_date,
                show_tops=show_tops,
                show_avg=show_avg,
                show_visibility=show_visibility,
            )
        except Exception as e:
            raise RuntimeError(f"Error while forming payload: {e}")

        return self.send_request(self.endpoints["summary_chart"], payload)

    def get_searchers_regions(
        self,
        project_id: int,
        searcher_key: Optional[int] = None,
        name_key: Optional[str] = None,
        country_code: Optional[str] = None,
        lang: Optional[str] = None,
        device: Optional[int] = None,
        depth: Optional[int] = None,
    ):
        """
        Exports a list of regions added to the project.
        :param project_id: Project ID.
        :param searcher_key: Search engine key.
        :param name_key: Name or region key.
        :param country_code: Two-letter country code.
        :param lang: Interface language.
        :param device: Device type (enum: 0, 1, 2).
        :param depth: Check depth.
        :return: Request result.
        """
        # Validate parameters
        if not isinstance(project_id, int):
            raise ValueError("project_id must be an integer.")
        if searcher_key and not isinstance(searcher_key, int):
            raise ValueError("searcher_key must be an integer.")
        if name_key and not isinstance(name_key, str):
            raise ValueError("name_key must be a string.")
        if country_code and (
            not isinstance(country_code, str) or len(country_code) != 2
        ):
            raise ValueError("country_code must be a two-letter country code.")
        if lang and not isinstance(lang, str):
            raise ValueError("lang must be a string.")
        if device is not None and device not in (0, 1, 2):
            raise ValueError("device must be one of the values: 0, 1, 2.")
        if depth is not None and not isinstance(depth, int):
            raise ValueError("depth must be an integer.")

        try:
            payload = PayloadFactory.positions_get_searchers_regions_payload(
                project_id=project_id,
                searcher_key=searcher_key,
                name_key=name_key,
                country_code=country_code,
                lang=lang,
                device=device,
                depth=depth,
            )
        except Exception as e:
            raise RuntimeError(f"Error while forming payload: {e}")

        return self.send_text_request(
            self.endpoints["searchers_regions_export"], payload
        )
