import pytest
import logging

from welkin.apps.polywood.noauth import pages

logger = logging.getLogger(__name__)


@pytest.mark.example
@pytest.mark.selenium
class PolywoodTests(object):
    """
        These selenium tests each call a selenium fixture that calls a fresh
        browser instance; that's an architectural decision, that every test
        starts fresh. You could just as easily use one browser session for
        *every* selenium test.

        This selenium fixture is scoped at the function level, and called
        by the test method as `driver`; that fixture is found on:
        welkin/tests/conftest.py::driver()

        pytest fixture documentation:
        https://docs.pytest.org/en/latest/fixture.html
    """

    def test_polywood_navigation(self, driver, polywood):
        """
            Simple navigation flow.

            Use a simple page object model that minimally manages page object
            transitions.

            Note: this is not an actual test, because it has no explicit
            assertions. However, the page object model is performing a
            lot of checks and validations in the background, which allows
            this test case to provide a fairly simple API to page interactions.
        """
        # we have a webdriver instance from this method's fixture `driver`,
        # which corresponds to the "browser" argument at the CLI invocation

        # instantiate the home page object
        home_page = pages.HomePage(driver, firstload=True)
        home_page.save_screenshot('home initialization')  # should be blank

        # load home page in browser and refresh the PO instance
        home_page = home_page.load()
        home_page.save_screenshot('home loaded')

        # get rid of the popup
        home_page.escape_popup()
        home_page.save_screenshot('home page after modal closed')

       # navigate to the "Categories" page
        categories_page = home_page.select_page_from_top_menu('Categories')
        categories_page.save_screenshot('categories page loaded')

       # navigate to the "Collections" page
        collections_page = categories_page.select_page_from_top_menu('Collections')
        collections_page.save_screenshot('collections page loaded')

       # navigate to the "Get Inspired" page
        get_inspired_page = collections_page.select_page_from_top_menu('Get Inspired')
        get_inspired_page.save_screenshot('get inspired page loaded')

       # navigate to the "Designer Series" page
        designer_series_page = get_inspired_page.select_page_from_top_menu('Designer Series')
        designer_series_page.save_screenshot('designer series page loaded')

        # get rid of the popup
        designer_series_page.escape_popup()
        designer_series_page.save_screenshot('designer series page after modal closed')

       # navigate to the "Showrooms" page
        showrooms_page = designer_series_page.select_page_from_top_menu('Showrooms')
        showrooms_page.save_screenshot('showrooms page loaded')

       # navigate back to the "Home" page
        home_page = showrooms_page.click_home_link()
        home_page.save_screenshot('home page loaded again')
