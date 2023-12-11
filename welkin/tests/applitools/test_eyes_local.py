import pytest
import logging

from selenium.common.exceptions import ElementClickInterceptedException
from applitools.selenium import Eyes
from welkin.apps.sweetshop.base_page import PomBootPage
from welkin.framework import utils

from applitools.selenium import Target

logger = logging.getLogger(__name__)


@pytest.mark.example
@pytest.mark.selenium
class ApplitoolsEyesTests(object):
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

    def test_linear_navigation(self, driver, sweetshop, eyes):
        """
            Simple navigation flow, with a simple page object model that
            minimally manages page object transitions.

            This test has simple assertions that validate the functional
            navigation. In addition, because it's an Eyes test, it visually
            validates the page states that corresponds to thet `eyes.check`
            statements. This means two things:
            1. navigation had to work to result in those page states
            2. the visual checks can examine the page beyond the limited
               explicit functional check points.

            This test method can be run in two ways:
            1. locally, but NOT specifying the grid
            >>>pytest tests/applitools -k test_linear_navigation --browser=headless_chrome

            2. on Aplitools UltraFast Grid
            >>>pytest tests/applitools -k test_linear_navigation --ultrafast_grid=yes --browser=headless_chrome


        """
        # we have a webdriver instance from this method's fixture `driver`,
        # which corresponds to the "browser" argument at the CLI invocation

        # instantiate the POM on the blank driver start page
        boot_page = PomBootPage(driver)

        # instantiate the home page object
        id = 'Home'
        home_page = boot_page.start_with('sweetshop home page')
        assert home_page.title == driver.title
        x, y = driver.get_window_size().values()
        dims = f"{x}_{y}"
        home_page.save_screenshot(f"{id.lower()} page loaded {dims}")

        # visual test!
        eyes.check(Target.window().fully().with_name(id))

        id = 'Sweets'
        sweets_page = home_page.select_page_from_top_menu(id)
        assert sweets_page.title == driver.title
        x, y = driver.get_window_size().values()
        dims = f"{x}_{y}"
        sweets_page.save_screenshot(f"{id.lower()} page loaded {dims}")

        # visual test!
        eyes.check(Target.window().fully().with_name(id))

        # id = 'About'
        # about_page = sweets_page.select_page_from_top_menu(id)
        # logger.info(f"\n>>>window size: {driver.get_window_size()}")
        # about_page.save_screenshot(f"{id.lower()} page loaded")
        # eyes.check(Target.window().fully().with_name(id))
        #
        # id = 'Login'
        # login_page = about_page.select_page_from_top_menu(id)
        # logger.info(f"\n>>>window size: {driver.get_window_size()}")
        # login_page.save_screenshot(f"{id.lower()} page loaded")
        # eyes.check(Target.window().fully().with_name(id))
        #
        # id = 'Basket'
        # basket_page = login_page.select_page_from_top_menu(id)
        # logger.info(f"\n>>>window size: {driver.get_window_size()}")
        # basket_page.save_screenshot(f"{id.lower()} page loaded")
        # eyes.check(Target.window().fully().with_name(id))
        #
        # # navigate back to the "Home" page
        # id = 'Home'
        # home_page = basket_page.select_page_from_top_menu(id)
        # logger.info(f"\n>>>window size: {driver.get_window_size()}")
        # home_page.save_screenshot(f"{id.lower()} page loaded again")
        # eyes.check(Target.window().fully().with_name(id))
        #
        # logger.info(f"\ndir(eyes): \n{utils.plog(dir(eyes))}")
        # logger.info(f"\neyes.__dict__: \n{utils.plog(eyes.__dict__)}")

        # logger.info(f"\neyes results:\n{utils.plog(eyes.get_results())}")

    @pytest.mark.parametrize('scenario',
                            [
                                ['Sweets', 'Login', 'About'],
                                ['About', 'Basket', 'Home'],
                                # ['Login', 'Home', 'Sweets'],
                                # ['Basket', 'About', 'Home'],  # expected broken link
                                # ['Basket', 'Sweets', 'Login'],
                                # ['Sweets', 'Basket', 'About'],  # expected broken link
                            ],
                            ids=['scenario01', 'scenario02']
                                 #'scenario03', 'scenario04', 'scenario05', 'scenario06']
    )
    def test_dynamic_navigation(self, driver, sweetshop, scenario, eyes):
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
            assert page.title == driver.title
            x, y = driver.get_window_size().values()
            dims = f"{x}_{y}"
            page.save_screenshot(f"{destination.lower()} page loaded {dims}")

            # visual test!
            eyes.check(Target.window().fully().with_name(destination))

