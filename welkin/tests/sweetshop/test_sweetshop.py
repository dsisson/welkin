import pytest
import logging

from welkin.apps.sweetshop.base_page import PomBootPage

logger = logging.getLogger(__name__)


@pytest.mark.example
@pytest.mark.selenium
class SweetshopTests(object):
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

    def test_linear_navigation(self, driver, sweetshop):
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

        # instantiate the POM on the blank driver start page
        boot_page = PomBootPage(driver)

        # instantiate the home page object
        home_page = boot_page.start_with('sweetshop home page')
        home_page.save_screenshot('home loaded')

        id = 'Sweets'
        sweets_page = home_page.select_page_from_top_menu(id)
        sweets_page.save_screenshot(f"{id.lower()} page loaded")

        id = 'About'
        about_page = sweets_page.select_page_from_top_menu(id)
        about_page.save_screenshot(f"{id.lower()} page loaded")

        id = 'Login'
        login_page = about_page.select_page_from_top_menu(id)
        login_page.save_screenshot(f"{id.lower()} page loaded")

        id = 'Basket'
        basket_page = login_page.select_page_from_top_menu(id)
        basket_page.save_screenshot(f"{id.lower()} page loaded")

        # navigate back to the "Home" page
        home_page = basket_page.select_page_from_top_menu('Home')
        home_page.save_screenshot('home page loaded again')

    @pytest.mark.parametrize('scenario',
                             [
                                 ['Sweets', 'Login', 'About'],
                                 ['About', 'Basket', 'Home'],
                                 ['Login', 'Home', 'Sweets'],
                                 ['Basket', 'About', 'Home'],  # expected broken link
                                 ['Basket', 'Sweets', 'Login'],
                                 ['Sweets', 'Basket', 'About'],  # expected broken link
                             ],
                             ids=['scenario01', 'scenario02', 'scenario03',
                                  'scenario04', 'scenario05', 'scenario06'])
    def test_dynamic_navigation(self, driver, sweetshop, scenario):
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

        # instantiate the POM on the blank driver start page
        boot_page = PomBootPage(driver)

        # instantiate the home page
        # to load any other page, we'd need to use its po id
        page = boot_page.start_with('sweetshop home page')
        page.save_screenshot('home loaded')

        for destination in scenario:
            logger.info(f"\nnavigating to {destination} page")
            page = page.select_page_from_top_menu(destination)
            page.save_screenshot(f"{destination.lower()} page loaded")
