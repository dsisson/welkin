import pytest
import logging

from welkin.apps.construct_connect.noauth import pages

logger = logging.getLogger(__name__)


@pytest.mark.example
@pytest.mark.selenium
class ConstructConnectTests(object):
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

    def test_linear_navigation(self, driver, construct_connect):
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

        id = 'Find More Bids'
        subcontractors_page = home_page.select_page_from_top_menu(id)
        subcontractors_page.save_screenshot(f"{id.lower()} page loaded")

        id = 'Quickly Create & Send Bid Invites'
        general_contractors_page = subcontractors_page.select_page_from_top_menu(id)
        general_contractors_page.save_screenshot(f"{id.lower()} page loaded")

        id = 'Bid Center'
        bid_center_page = general_contractors_page.select_page_from_top_menu(id)
        bid_center_page.save_screenshot(f"{id.lower()} page loaded")

        id = 'Grab the Survival Kit'
        survival_kit_page = bid_center_page.select_page_from_top_menu(id)
        survival_kit_page.save_screenshot(f"{id.lower()} page loaded")

        id = 'Careers'
        careers_page = survival_kit_page.select_page_from_top_menu(id)
        careers_page.save_screenshot(f"{id.lower()} page loaded")

        # navigate back to the "Home" page
        home_page = careers_page.select_page_from_top_menu('Home')
        home_page.save_screenshot('home page loaded again')

    @pytest.mark.parametrize('scenario',
                            [
                                ['Find More Bids', 'Careers', 'Bid Center'],
                                ['Grab the Survival Kit', 'Find More Bids', 'Quickly Create & Send Bid Invites'],
                                ['Bid Center', 'Home', 'Grab the Survival Kit'],
                                ['Find More Bids', 'Quickly Create & Send Bid Invites', 'Careers'],
                                ['Grab the Survival Kit', 'Careers', 'Home']
                            ],
                            ids=['scenario01', 'scenario02', 'scenario03',
                                 'scenario04', 'scenario05']
    )
    def test_dynamic_navigation(self, driver, construct_connect, scenario):
        """
            Dynamic navigation flows. Visit the pages specified in
            the fixture parameter `scenario`.

            Use a simple page object model that minimally manages page object
            transitions.

            Note: this is not an actual test, because it has no explicit
            assertions. However, the page object model is performing a
            lot of checks and validations in the background, which allows
            this test case to provide a fairly simple API to page interactions.
        """
        # we have a webdriver instance from this method's fixture `driver`,
        # which corresponds to the "browser" argument at the CLI invocation

        msg = f"testing navigation path: \nHome --> {'--> '.join(scenario)}"
        logger.info(f"\n{'#' * 60}\n{msg}\n{'#' * 60}\n")

        # instantiate the home page object
        # every scenario starts with the home page
        page = pages.HomePage(driver, firstload=True)
        page.save_screenshot('home initialization')  # should be blank

        # load home page in browser and refresh the PO instance
        page = page.load()
        page.save_screenshot('home loaded')

        for destination in scenario:
            logger.info(f"\nnavigating to {destination} page")
            page = page.select_page_from_top_menu(destination)
            page.save_screenshot(f"{destination.lower()} page loaded")
