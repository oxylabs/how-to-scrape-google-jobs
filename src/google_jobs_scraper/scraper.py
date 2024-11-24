"""
    Module for scraping Google Jobs.
"""

import logging
import time

from typing import List

from pydantic import ValidationError
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from google_jobs_scraper.conf import google_jobs_scraper_settings
from google_jobs_scraper.models import Job


logging.getLogger("WDM").setLevel(logging.ERROR)


class ConsentFormAcceptError(BaseException):
    message = "Unable to accept Google consent form."


class DriverInitializationError(BaseException):
    message = "Unable to initialize Chrome webdriver for scraping."


class DriverGetJobsDataError(BaseException):
    message = "Unable to get Google Jobs data with Chrome webdriver."


class GoogleJobsScraper:
    """Class for scraping Google Jobs"""

    def __init__(self, logger: logging.Logger | None = None) -> None:
        self._logger = logger if logger else logging.getLogger(__name__)
        self._consent_button_xpath = "/html/body/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/div[1]/form[2]/div/div/button/span"

    def _init_chrome_driver(self) -> webdriver.Chrome:
        """Initializes Chrome webdriver"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        service = Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=chrome_options)

    def _click_consent_button(self, driver: webdriver.Chrome, query: str) -> None:
        """Clicks google consent form with selenium Chrome webdriver"""
        self._logger.info("Accepting consent form..")
        url = google_jobs_scraper_settings.get_jobs_url(query)
        try:
            driver.get(url)
            consent_button = driver.find_element(
                By.XPATH,
                self._consent_button_xpath,
            )
            consent_button.click()
        except NoSuchElementException:
            self._logger.warning("Consent form button not found.")
        except Exception as e:
            raise ConsentFormAcceptError from e

        time.sleep(2)

    def _get_data_from_item_div(self, div: webdriver.Chrome) -> Job:
        """Retrieves jobs data from a div element and returns it as a Job object."""
        title = div.find_element(By.CLASS_NAME, "tNxQIb").text
        company = div.find_element(By.CLASS_NAME, "a3jPc").text
        location = div.find_element(By.CLASS_NAME, "FqK3wc").text
        url = div.find_element(By.CLASS_NAME, "MQUd2b").get_attribute("href")
        return Job(
            title=title,
            company=company,
            location=location,
            url=url,
        )

    def _get_items_for_query(self, driver: webdriver.Chrome) -> List[Job]:
        """Retrieves Jobs item data from a Google Jobs page."""
        self._logger.info("Scraping Google Jobs page..")
        time.sleep(3)

        items = driver.find_elements(By.CLASS_NAME, "EimVGf")
        item_data = []
        for div in items:
            try:
                item = self._get_data_from_item_div(div)
            except ValidationError:
                self._logger.error("Data missing from jobs item div. Skipping..")
                continue

            item_data.append(item)

        return item_data

    def get_jobs_data_for_query(self, query: str) -> List[Job]:
        """
        Retrieves a list of Jobs items in Google Jobs for a query.

        Returns:
            List[Job]: A list of Job objects.
        Raises:
            ConsentFormAcceptError: If the Google consent form cannot be accepted.
            DriverInitializationError: If the Chrome webdriver cannot be initialized.
            DriverGetJobsDataError: If the Jobs data cannot be scraped from the Google Jobs site.
        """
        self._logger.info(f"Retrieving jobs for query {query}..")
        try:
            driver = self._init_chrome_driver()
        except Exception as e:
            raise DriverInitializationError from e

        try:
            self._click_consent_button(driver, query)
        except Exception as e:
            driver.close()
            raise e

        try:
            return self._get_items_for_query(driver)
        except Exception as e:
            raise DriverGetJobsDataError from e
        finally:
            driver.close()
