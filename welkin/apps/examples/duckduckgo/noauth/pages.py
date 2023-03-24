import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from welkin.apps.examples.duckduckgo.noauth.base_noauth import NoAuthBasePageObject
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
        self._set_field_input(search_input, 'search field', text,
                              clear=False, click=True, unfocus=False)

        # submit the search
        self._submit_form_submit(search_input, 'search field')

        # wait for the next page to render
        wait = WebDriverWait(self.driver, 10)
        url_escaped_query = text.replace(' ', '+')
        logger.info(f"\nurl_escaped_query: {url_escaped_query}")
        try:
            wait.until(EC.url_contains(f"q={url_escaped_query}"))
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


class ExternalHomePage(BasePage):
    """
        There are two different forms of the home page, with slightly
        different elements:
            1. the page at https://duckduckgo.com/
            2. the page at https://duckduckgo.com/?t=h_, which is reached by
               clicking a link to the home page

        This makes it a bit challenging to identify selectors for identity
        and load between the two. This is distinct from the firtload issues
        noted in __init__().
    """
    name = 'duckduckgo external home page'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.ID, 'searchbox_homepage')
    ]
    unload_checks = []

    def __init__(self, driver):
        """
            Because this is a start page for the application, it needs
            some special handling:
            1. an __init__ arg `firstload` that has to be set as True
               from the test code for the first invocation of the POM.
            2. clearing out the unload_checks if firstload=True

            This special handling works around the fact that the start
            page gets double-loaded, and so the first load can't perform
            unload checks!

            :param driver: webdriver instance
            :param firstload: bool, True if this is a start page first load
        """
        self.url = 'https://' + self.domain
        self.driver = driver
        self.title = f"{self.appname} — Privacy, simplified."
        logger.info(f"\n-----> unload checks: {self.unload_checks}")
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


class InternalHomePage(BasePage):
    """
        There are two different forms of the home page, with slightly
        different elements:
            1. the page at https://duckduckgo.com/
            2. the page at https://duckduckgo.com/?t=h_, which is reached by
               clicking a link to the home page

        This makes it a bit challenging to identify selectors for identity
        and load between the two. This is distinct from the firtload issues
        noted in __init__().
    """
    name = 'duckduckgo internal home page'
    identity_checks = ['check_url', 'check_title']
    load_checks = [
        (True, By.ID, 'search_form_input_homepage')
    ]
    unload_checks = [
        (False, By.ID, 'search_form_input_homepage')
        # title check dynamically added by __init__()
    ]

    def __init__(self, driver):
        self.driver = driver
        self.title = f"{self.appname} — Privacy, simplified."
        self.url = self.driver.current_url
        logger.info('\n' + INIT_MSG % self.name)


class SearchResultsPage(BasePage):

    name = 'duckduckgo search results page'
    identity_checks = ['check_url_chunks', 'check_title']
    load_checks = [
        (True, By.ID, 'search_form_input')
        # title check dynamically added by __init__()
    ]
    unload_checks = []

    def __init__(self, driver, text):
        self.driver = driver
        self.search_text = text
        self.title = f"{self.search_text} at {self.appname}"
        self.url_chunks = [f"https://{self.domain}/", f"q={self.search_text.replace(' ', '+')}"]
        # because the title is set in __init__(),
        # the check also has to be set and added here
        titlecheck = (False, By.XPATH, f"//title[text()='{self.title}']")
        self.load_checks.append(titlecheck)
        self.url = self.driver.current_url
        logger.info('\n' + INIT_MSG % self.name)

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
