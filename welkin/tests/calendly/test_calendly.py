import pytest
import logging

from welkin.apps.calendly.noauth import pages

logger = logging.getLogger(__name__)


@pytest.mark.example
@pytest.mark.selenium
class calendlyTests(object):
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

    def test_calendly_navigation(self, driver, calendly):
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

        # navigate to the "Product" page
        products_page = home_page.select_page_from_top_menu('Products')
        products_page.save_screenshot('products page loaded')

        # navigate to the "Solutions" page
        solutions_page = products_page.select_page_from_top_menu('Solutions')
        solutions_page.save_screenshot('solutions page loaded')

        # navigate to the "Teams & Companies" page
        teams_page = solutions_page.select_page_from_top_menu('Teams & Companies')
        teams_page.save_screenshot('team page loaded')

        # navigate to the "Pricing" page
        pricing_page = teams_page.select_page_from_top_menu('Pricing')
        pricing_page.save_screenshot('pricing page loaded')

        # navigate to the "Resources" page
        resources_page = pricing_page.select_page_from_top_menu('Resources')
        resources_page.save_screenshot('resources page loaded')

        # navigate back to the "Home" page
        home_page = resources_page.select_page_from_top_menu('Home')
        home_page.save_screenshot('home page loaded again')
