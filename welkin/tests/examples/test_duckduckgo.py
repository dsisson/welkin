import pytest
import logging
import time

from welkin.framework.exceptions import PageIdentityException
from welkin.framework import utils
from welkin.apps.examples.duckduckgo_limited import limited_pages as lPOs
from welkin.apps.examples.duckduckgo_simple import simple_pages as sPOs
from welkin.apps.examples.duckduckgo.noauth import pages as POs

logger = logging.getLogger(__name__)


@pytest.mark.example
@pytest.mark.selenium
class ExampleDuckduckgoTests(object):
    """
        These selenium tests each call a selenium fixture that calls a fresh
        browser instance; that's an architectural decision, that every test
        starts fresh. You could just as easily use one browsersession for
        *every* selenium test.

        This selenium fixture is scoped at the function level, and called
        by the test method as `driver'; that fixture is found on:
        welkin/tests/conftest.py::driver()

        pytest fixture documentation:
        https://docs.pytest.org/en/latest/fixture.html
    """
    def test_duckduckgo_brittle(self, driver):
        """
            Using a correctly-spelled query string, validate some results data
            test points on the search results page, but do everything the
            brittle way, with non-abstracted selenium code.
        """
        # we have a webdriver instance from this method's fixture `driver`,
        # which corresponds to the "browser" argument at the CLI invocation

        # load home page
        driver.get('https://duckduckgo.com')

        # verify that we are on the correct page
        # set expectations
        expected_title = 'DuckDuckGo — Privacy, simplified.'
        expected_domain = 'duckduckgo.com'

        # actual results
        domain_from_url = driver.current_url.split('/')
        actual_title = driver.title
        actual_domain = domain_from_url[2]

        # validate expectations
        if not (actual_title == expected_title
                and actual_domain == expected_domain):
            msg1 = 'ERROR: DuckDuckGo home page did NOT self-validate identity. '
            msg2 = 'Expected "%s" + "%s", got "%s" + "%s".' % \
                   (expected_title, expected_domain, actual_title, actual_domain)
            logger.error(msg1 + msg2)
            raise PageIdentityException(msg1 + msg2)

        # perform search
        search_input = driver.find_element_by_class_name('js-search-input')

        # pass in the search string
        query = 'test case design in python'
        search_input.send_keys(query)

        # submit the search
        search_input.submit()

        time.sleep(5)

        # by now, the search results page should have loaded in the browser,
        # so now we need verify that.
        # set expectations
        expected_title = f"{'test case design in python'} at DuckDuckGo"
        expected_url = f"https://duckduckgo.com/?q={query.replace(' ', '+')}"

        # actual results
        actual_title = driver.title
        actual_url = driver.current_url.split('&')[0]

        # validate expectations
        if not (actual_title == expected_title and actual_url == expected_url):
            msg1 = f"ERROR: DuckDuckGo search results page did NOT " \
                   f"self-validate identity. "
            msg2 = f"Expected '{expected_title}' + '{expected_url}', " \
                   f"got '{actual_title}' + '{actual_url}'."
            logger.error(msg1 + msg2)
            raise PageIdentityException(msg1 + msg2)

        raw_results = driver.find_elements_by_class_name('js-result-title-link')
        result_titles = [item.text for item in raw_results]

        # some checkpoints to validate search results
        # 1. we should have some results
        assert len(result_titles) > 0, f"No results found for '{query}'"

        # 2. at least some of the results should be somewhat relevant
        raw_relevant_results = []
        for token in query.split(' '):
            for title in result_titles:
                if token.lower() in title.lower():
                    raw_relevant_results.append(title)
        relevant_results = list(set(raw_relevant_results))  # de-dupe
        logger.info(f"\nrelevant results:\n{utils.plog(relevant_results)}")
        assert len(relevant_results) > 5, \
            f"Only {len(relevant_results)} relevant results found, hoped for 5"

        # clean up
        driver.quit()

    def test_duckduckgo_limited(self, driver):
        """
            Using a correctly-spelled query string, validate some results data
            test points on the search results page.

            Use a limited page object model that does not manage page object
            transitions; perform those manually in the test case.
        """
        # we have a webdriver instance from this method's fixture `driver`,
        # which corresponds to the "browser" argument at the CLI invocation

        query = 'test case design in python'

        # instantiate the home page object
        home_page = lPOs.HomePage(driver)

        # load home page
        home_page.load()

        # verify that we are on the correct page
        home_page.verify_self()

        # perform search
        home_page.search_for(query)

        # the browser should have changed to the search results page;
        # now we have to sync up the test case to a page object that
        # corresponds to that results page
        results_page = lPOs.SearchResultsPage(driver, query)

        # verify that we are on the correct page
        results_page.verify_self()

        # get the search results titles
        result_titles = results_page.scrape_results_list()

        # some checkpoints to validate search results
        # 1. we should have some results
        assert len(result_titles) > 0, f"No results found for '{query}'"

        # 2. at least some of the results should be somewhat relevant
        raw_relevant_results = []
        for token in query.split(' '):
            for title in result_titles:
                if token.lower() in title.lower():
                    raw_relevant_results.append(title)
        relevant_results = list(set(raw_relevant_results))  # de-dupe
        logger.info(f"\n{len(relevant_results)} relevant results:\n{utils.plog(relevant_results)}")
        assert len(relevant_results) > 5, \
            f"Only {len(relevant_results)} relevant results found, hoped for 5"

    def test_duckduckgo_simple(self, driver):
        """
            Using a correctly-spelled query string, validate some results data
            test points on the search results page.

            Use a simple page object model that minimally manages page object
            transitions.
        """
        # we have a webdriver instance from this method's fixture `driver`,
        # which corresponds to the "browser" argument at the CLI invocation

        query = 'test case design in python'

        # instantiate the home page object
        home_page = sPOs.HomePage(driver)

        # load home page
        home_page.load()

        # verify that we are on the correct page
        home_page.verify_self()

        # perform search, which returns a page object for the results page
        results_page = home_page.search_for(query)

        # verify that we are on the correct page
        results_page.verify_self()

        # get the search results titles
        result_titles = results_page.scrape_results_list()

        # some checkpoints to validate search results
        # 1. we should have some results
        assert len(result_titles) > 0, f"No results found for '{query}'"

        # 2. at least some of the results should be somewhat relevant
        raw_relevant_results = []
        for token in query.split(' '):
            for title in result_titles:
                if token.lower() in title.lower():
                    raw_relevant_results.append(title)
        relevant_results = list(set(raw_relevant_results))  # de-dupe
        logger.info(f"\n{len(relevant_results)} relevant results:\n{utils.plog(relevant_results)}")
        assert len(relevant_results) > 5, \
            f"Only {len(relevant_results)} relevant results found, hoped for 5"

    def test_duckduckgo_router(self, driver):
        """
            Using a correctly-spelled query string, validate some results data
            test points on the search results page.

            Use a simple page object model that minimally manages page object
            transitions.
        """
        # we have a webdriver instance from this method's fixture `driver`,
        # which corresponds to the "browser" argument at the CLI invocation

        query = 'test case design in python'

        # instantiate the home page object
        home_page = POs.HomePage(driver, firstload=True)
        home_page.save_screenshot('home initialization')  # should be blank

        # load home page in browser and refresh the PO instace
        home_page = home_page.load()
        home_page.save_screenshot('home loaded')

        # perform search, which returns a page object for the results page
        results_page = home_page.search_for(query)
        results_page.save_screenshot('results after search')

        # get the search results titles
        result_titles = results_page.scrape_results_list()

        # some checkpoints to validate search results
        # 1. we should have some results
        assert len(result_titles) > 0, f"No results found for '{query}'"

        # 2. at least some of the results should be somewhat relevant
        raw_relevant_results = []
        for token in query.split(' '):
            for title in result_titles:
                if token.lower() in title.lower():
                    raw_relevant_results.append(title)
        relevant_results = list(set(raw_relevant_results))  # de-dupe
        logger.info(f"\n{len(relevant_results)} relevant results:\n{utils.plog(relevant_results)}")
        assert len(relevant_results) > 5, \
            f"Only {len(relevant_results)} relevant results found, hoped for 5"
