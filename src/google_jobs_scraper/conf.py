"""
    Config module for google_jobs_scraper.
"""

from urllib.parse import quote

from pydantic_settings import BaseSettings


class GoogleJobsScraperSettings(BaseSettings):
    """Settings class for Google Jobs Scraper"""

    url: str = "https://www.google.com/search?ibp=htl;jobs&hl=en&gl=us"

    def get_jobs_url(self, query: str) -> str:
        """Returns a Google Jobs URL for a given query string."""
        encoded_query = quote(query)
        return f"{self.url}&q={encoded_query}"


google_jobs_scraper_settings = GoogleJobsScraperSettings()
