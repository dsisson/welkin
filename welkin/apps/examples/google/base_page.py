
import logging
import pytest
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logger = logging.getLogger(__name__)


class PageObject(object):

    domain = 'www.google.com'

    def search_for(self, text):
        """
            Perform a Google search for string `text`.

            :param text: str, query string
            :return page: page Welkin page object for the search results page
        """
        # grab the search field
        search_input = self.driver.find_element_by_name('q')

        # pass in the search string
        search_input.send_keys(text)

        # submit the search
        search_input.submit()

        # instantiate a search results page
        from welkin.apps.examples.google.results import SearchResultsPage
        page = SearchResultsPage(self.driver)

        return page
