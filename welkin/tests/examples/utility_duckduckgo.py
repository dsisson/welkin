import logging
import time

from selenium import webdriver

from welkin.apps.examples.duckduckgo.noauth import pages as POs

logger = logging.getLogger(__name__)


def naive_duckduckgo_pageobjects():
    """
        An example of how to use a naive POM from a script
        that is NOT a test case, and does NOT use pytest.

        to run:
            >>> pwd
            /Users/derek/dev/welkin/welkin
            >>>  python tests/examples/utility_duckduckgo.py
    """
    driver = webdriver.Chrome()

    query = 'test case design in python'

    # instantiate page object model for google.com
    home_page = POs.HomePage(driver)

    # load home page
    home_page.load()
    time.sleep(5)  # anti-pattern!

    # verify that we are on the correct page
    # this will throw an exception if the page is not correct
    home_page.verify_self()

    # perform search
    home_page.search_for(query)
    time.sleep(5)  # anti-pattern!

    # instantiate page object for search results page
    results_page = POs.SearchResultsPage(driver, query)

    # verify that we are on the correct page
    # this will throw an exception if the page is not correct
    results_page.verify_self()

    results_list = results_page.scrape_results_list()
    print(f"number of results: {len(results_list)}")
    for i, result in enumerate(results_list):
        print(i, result)


if __name__ == "__main__":
    naive_duckduckgo_pageobjects()
