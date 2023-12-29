import logging
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

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
            :return page: Welkin page object for the search results page
        """
        # different pages have different search form selectors; grab every
        # element with an id that starts with "search"
        possible_elements = self.driver.find_elements(By.CSS_SELECTOR, '[id^=search')
        sel_search_form = None
        for e in possible_elements:
            # find the *first* id that ends with 'input'
            this_id = e.get_property('id')
            if this_id.endswith('input'):
                sel_search_form = this_id
                break

        # grab the search field
        wait = WebDriverWait(self.driver, 10)
        try:
            wait.until(EC.presence_of_element_located((By.ID, sel_search_form)))
        except TimeoutException:
            self.save_screenshot(f"form not found {self.name}")
            raise

        search_input = self.driver.find_element(By.ID, sel_search_form)

        # pass in the search string
        search_input.send_keys(text)

        # submit the search
        search_input.submit()

        # wait for the next page to render
        wait = WebDriverWait(self.driver, 10)
        url_escaped_query = text.replace(' ', '+')
        try:
            wait.until(EC.url_contains(f"q={url_escaped_query}"))
        except TimeoutException:
            logger.info(f"\ncurrent_url: {self.driver.current_url}")
            raise
        wait.until(EC.visibility_of_all_elements_located((By.ID, 'links')))
        logger.info('wait succeeded')

        # instantiate a search results page
        page = SearchResultsPage(self.driver, text)
        return page


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
        # expected_url = f"https://{self.domain}/?q={self.search_text.replace(' ', '+')}"
        expected_escaped_query_in_url = f"q={self.search_text.replace(' ', '+')}"

        # actual results
        actual_title = self.driver.title
        actual_url = self.driver.current_url

        # validate expectations
        if actual_title == expected_title and expected_escaped_query_in_url in actual_url:
            msg = f"{self.appname} search results page self-validated identity."
            logger.info(msg)
            return True
        else:
            msg1 = f"\nFAIL: {self.appname} search results page did NOT " \
                   f"self-validate identity. "
            msg2 = f"\nExpected '{expected_title}' + '{expected_escaped_query_in_url}', " \
                   f"got '{actual_title}' + '{actual_url}'."
            logger.error(msg1 + msg2)
            raise PageIdentityException(msg1 + msg2)

    def scrape_results_list(self):
        """
            Pull out the document titles, which may be displayed as truncated.

            :return result_titles: list, str titles for each returned result
        """
        sel_result_items = 'article div:nth-child(2)'
        raw_results = self.driver.find_elements(By.CSS_SELECTOR, sel_result_items)
        result_titles = [item.text for item in raw_results]
        logger.info(f"\nSearch results item titles:\n{utils.plog(result_titles)}")
        return result_titles
