import logging
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from welkin.apps.examples.duckduckgo.noauth.base_noauth import NoAuthBasePageObject
from welkin.framework.exceptions import PageIdentityException
from welkin.framework import utils

logger = logging.getLogger(__name__)
INIT_MSG = 'Instantiated PageObject for %s.'


class BasePage(NoAuthBasePageObject):

    appname = 'DuckDuckGo'
    domain = 'duckduckgo.com'

    def search_for(self, text):
        """
            Perform a DuckDuckGo search for string `text`.

            :param text: str, query string
            :return page: page object for the search results page
        """
        sel_search_form = 'js-search-input'
        # grab the search field
        search_input = self.driver.find_element(By.CLASS_NAME, sel_search_form)

        # pass in the search string
        search_input.send_keys(text)

        # submit the search
        search_input.submit()

        # wait for the next page to render
        wait = WebDriverWait(self.driver, 10)
        url_escaped_query = text.replace(' ', '+')
        try:
            wait.until(EC.url_contains(f"?q={url_escaped_query}"))
        except TimeoutException:
            logger.info(f"\ncurrent_url: {self.driver.current_url}")
            raise
        wait.until(EC.visibility_of_all_elements_located((By.ID, 'links')))
        logger.info('wait succeeded')

        # instantiate and return a search results page
        opts = {'text': text}
        po_selector = 'duckduckgo search results page'
        page = self.load_pageobject(po_selector, **opts)
        return page


class HomePage(BasePage):

    name = 'duckduckgo home page'
    identity_checks = ['check_url', 'check_title']

    def __init__(self, driver):
        self.url = 'https://' + self.domain
        self.driver = driver
        self.title = f"{self.appname} — Privacy, simplified."
        logger.info('\n' + INIT_MSG % self.name)

    def load(self):
        """
            Get and load the home page for DuckDuckGo search in the browser
            and instantiate and return a page object for the home page.

            In the log record, you will see this page object instantiated
            twice, because the test case called HomePage, and then
            load() called HomePage again to change the browser to the
            appropriate URL.

            :return page: page object for the home page
        """
        self.driver.get(self.url)
        logger.info(f"\nLoaded {self.appname} home page to url '{self.url}'.")

        # instantiate and return a refreshed PO
        po_selector = self.name
        page = self.load_pageobject(po_selector)
        return page


class SearchResultsPage(BasePage):

    name = 'duckduckgo search results page'
    identity_checks = ['check_url', 'check_title']

    def __init__(self, driver, text):
        self.driver = driver
        self.search_text = text
        self.title = f"{self.search_text} at {self.appname}"
        self.url = f"https://{self.domain}/?q={self.search_text.replace(' ', '+')}"
        time.sleep(4)  # wait for page to load
        logger.info('\n' + INIT_MSG % self.name)

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
