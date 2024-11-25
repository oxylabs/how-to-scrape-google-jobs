"""
    Main module for google_jobs_scraper.
"""

import logging

import click

from google_jobs_scraper.collector import GoogleJobsDataCollector


logging.basicConfig(level=logging.INFO)


@click.command()
@click.option(
    "--query",
    help="The query for which to return Google Jobs results for.",
    required=True,
)
def scrape_google_jobs(query: str) -> None:
    collector = GoogleJobsDataCollector()
    collector.save_jobs_data_for_query(query)


if __name__ == "__main__":
    scrape_google_jobs()
