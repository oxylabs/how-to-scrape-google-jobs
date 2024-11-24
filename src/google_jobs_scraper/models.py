"""
    Pydantic models for Google Jobs scraper.
"""

from pydantic import BaseModel


class Job(BaseModel):
    title: str
    company: str
    location: str
    url: str
