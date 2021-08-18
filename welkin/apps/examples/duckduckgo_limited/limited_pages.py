import logging
import time

from selenium.webdriver.common.by import By

from welkin.framework.exceptions import PageIdentityException
from welkin.framework import utils

logger = logging.getLogger(__name__)


class BasePageObject(object):

    appname = 'DuckDuckGo'
    domain = 'duckduckgo.com'

    def search_for(self, text):
        """
            Perform a DuckDuckGo search for string `text`.

            :param text: str, query string
            :return: None
        """
        sel_search_form = 'js-search-input'
        # grab the search field
        search_input = self.driver.find_element(By.CLASS_NAME, sel_search_form)

        # pass in the search string
        search_input.send_keys(text)

        # submit the search
        search_input.submit()


class HomePage(BasePageObject):

    def __init__(self, driver):
        self.url = 'https://' + self.domain
        self.driver = driver
        logger.info(f"Instantiated PageObject for {self.appname}.")

    def load(self):
        """
            Get and load the home page for DuckDuckGo search.

            :return: None
        """
        self.driver.get(self.url)
        logger.info(f"Loaded {self.appname} home page.")

    def verify_self(self):
        """
            Check these specific identifiers to prove that
            we are on the expected page.

            :return: True if valid, else raise exception
        """
        # set expectations
        expected_title = f"{self.appname} — Privacy, simplified."
        expected_domain = self.domain

        # actual results
        domain_from_url = self.driver.current_url.split('/')
        actual_title = self.driver.title
        actual_domain = domain_from_url[2]

        # validate expectations
        if actual_title == expected_title and actual_domain == expected_domain:
            logger.info(f"{self.appname} home page self-validated identity.")
            return True
        else:
            msg1 = f"FAIL: {self.appname} home page did NOT self-validate identity. "
            msg2 = f"Expected '{expected_title}' + '{expected_domain}', " \
                   f"got '{actual_title}' + '{actual_domain}'."
            logger.error(msg1 + msg2)
            raise PageIdentityException(msg1 + msg2)


class SearchResultsPage(BasePageObject):

    def __init__(self, driver, text):
        self.driver = driver
        self.search_text = text
        time.sleep(4)  # wait for page to load
        logger.info(f"Instantiated {self.appname} search results PageObject.")

    def verify_self(self):
        """
            Check these specific identifiers to prove that
            we are on the expected page.

            :return: True if valid, else raise exception
        """
        # set expectations
        expected_title = f"{self.search_text} at {self.appname}"
        expected_url = f"https://{self.domain}/?q={self.search_text.replace(' ', '+')}"

        # actual results
        actual_title = self.driver.title
        actual_url = self.driver.current_url

        # validate expectations
        if actual_title == expected_title and actual_url.startswith(expected_url):
            msg = f"{self.appname} search results page self-validated identity."
            logger.info(msg)
            return True
        else:
            msg1 = f"FAIL: {self.appname} search results page did NOT " \
                   f"self-validate identity. "
            msg2 = f"Expected '{expected_title}' + '{expected_url}', " \
                   f"got '{actual_title}' + '{actual_url}'."
            logger.error(msg1 + msg2)
            raise PageIdentityException(msg1 + msg2)

    def scrape_results_list(self):
        """
            Pull out the document titles, which may be displayed as truncated.

            :return result_titles: list, str titles for each returned result
        """
        sel_result_items = 'js-result-title-link'
        raw_results = self.driver.find_elements(By.CLASS_NAME, sel_result_items)
        result_titles = [item.text for item in raw_results]
        logger.info(f"\nSearch results item titles:\n{utils.plog(result_titles)}")
        return result_titles
