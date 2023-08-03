import pytest
import logging

from welkin.apps.leolabs.noauth import pages

logger = logging.getLogger(__name__)


@pytest.mark.example
@pytest.mark.selenium
class LeoLabsTests(object):
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

    def test_linear_navigation(self, driver, leolabs):
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

        id = 'LeoTrack'
        leotrack_page = home_page.select_page_from_top_menu(id)
        leotrack_page.save_screenshot(f"{id.lower()} page loaded")

        id = 'Our Radars'
        radars_page = leotrack_page.select_page_from_top_menu(id)
        radars_page.save_screenshot(f"{id.lower()} page loaded")

        id = 'Our Vertex'
        vertex_page = radars_page.select_page_from_top_menu(id)
        vertex_page.save_screenshot(f"{id.lower()} page loaded")

        id = 'Regulators'
        regulators_page = vertex_page.select_page_from_top_menu(id)
        regulators_page.save_screenshot(f"{id.lower()} page loaded")

        id = 'Insurers'
        insurers_page = regulators_page.select_page_from_top_menu(id)
        insurers_page.save_screenshot(f"{id.lower()} page loaded")

        id = 'LeoPulse'
        leopulse_page = insurers_page.select_page_from_top_menu(id)
        leopulse_page.save_screenshot(f"{id.lower()} page loaded")

        id = 'About Us'
        about_page = leopulse_page.select_page_from_top_menu(id)
        about_page.save_screenshot(f"{id.lower()} page loaded")

        # navigate back to the "Home" page
        home_page = about_page.select_page_from_top_menu('Home')
        home_page.save_screenshot('home page loaded again')

    @pytest.mark.parametrize('scenario',
                            [
                                ['LeoTrack', 'LeoPulse', 'About Us'],
                                ['Our Radars', 'About Us', 'Our Radars'],
                                ['Insurers', 'LeoPulse', 'Our Radars'],
                                ['Regulators', 'LeoTrack', 'Insurers'],
                                ['Our Vertex', 'Regulators', 'LeoPulse'],
                            ],
                            ids=['scenario01', 'scenario02', 'scenario03',
                                 'scenario04', 'scenario05']
    )
    def test_dynamic_navigation(self, driver, leolabs, scenario):
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
