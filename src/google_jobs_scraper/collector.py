"""
    Main module for collecting Google Jobs data.
"""

import logging

from typing import List

import pandas as pd

from google_jobs_scraper.models import Job
from google_jobs_scraper.scraper import GoogleJobsScraper


DEFAULT_OUTPUT_FILE = "jobs.csv"


class GoogleJobsDataCollector:
    """Data collector class for Google Jobs"""

    def __init__(
        self,
        output_file: str | None = None,
        logger: logging.Logger | None = None,
    ) -> None:
        self._scraper = GoogleJobsScraper()
        self._output_file = output_file if output_file else DEFAULT_OUTPUT_FILE
        self._logger = logger if logger else logging.getLogger(__name__)

    def _save_to_csv(self, jobs: List[Job]) -> None:
        """Saves given list of jobs to a CSV file."""
        self._logger.info(f"Writing {len(jobs)} jobs to {self._output_file}..")
        jobs = [job.model_dump() for job in jobs]
        df = pd.DataFrame(jobs)
        df.to_csv(self._output_file)

    def save_jobs_data_for_query(self, query: str) -> None:
        """
        Scrapes data from Google Jobs for a given query string and stores it into a CSV file.

        Args:
            query (str): The query string for which to get jobs results.
        """
        self._logger.info(f"Getting Google Jobs data for query {query}..")
        try:
            items = self._scraper.get_jobs_data_for_query(query)
        except Exception:
            self._logger.exception(
                f"Error when scraping Google Jobs for query {query}."
            )
            return

        if not items:
            self._logger.info("No items found for query.")
            return

        self._save_to_csv(items)
