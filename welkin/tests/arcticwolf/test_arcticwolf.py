import pytest
import logging

from welkin.apps.arcticwolf.base_page import PomBootPage

logger = logging.getLogger(__name__)


@pytest.mark.example
@pytest.mark.selenium
class ArcticWolfTests(object):
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

    def test_linear_navigation(self, driver, arcticwolf):
        """
            Simple navigation flow, using a simple page object model that
            minimally manages page object transitions.

            Note: the page object model is performing a lot of checks and
            validations in the background, which allows this test case to
            provide
            a fairly simple API to page interactions.
        """
        # we have a webdriver instance from this method's fixture `driver`,
        # which corresponds to the "browser" argument at the CLI invocation

        # instantiate the POM on the blank driver start page
        boot_page = PomBootPage(driver)

        # instantiate the home page object
        home_page = boot_page.start_with('arcticwolf home page')
        home_page.save_screenshot('home loaded')
        assert driver.title == home_page.title

        id = 'Solutions'
        solutions_page = home_page.select_page_from_top_menu(id)
        solutions_page.save_screenshot(f"{id.lower()} page loaded")
        assert driver.title == solutions_page.title

        id = 'How It Works'
        howitworks_page = solutions_page.select_page_from_top_menu(id)
        howitworks_page.save_screenshot(f"{id.lower()} page loaded")
        assert driver.title == howitworks_page.title

        id = 'Why Arctic Wolf'
        why_page = howitworks_page.select_page_from_top_menu(id)
        why_page.save_screenshot(f"{id.lower()} page loaded")
        assert driver.title == why_page.title

        id = 'Resources'
        resources_page = why_page.select_page_from_top_menu(id)
        resources_page.save_screenshot(f"{id.lower()} page loaded")
        assert driver.title == resources_page.title

        id = 'Solution Providers'
        providers_page = resources_page.select_page_from_top_menu(id)
        providers_page.save_screenshot(f"{id.lower()} page loaded")
        assert driver.title == providers_page.title

        id = 'Leadership'
        leadership_page = providers_page.select_page_from_top_menu(id)
        leadership_page.save_screenshot(f"{id.lower()} page loaded")
        assert driver.title == leadership_page.title

        id = 'Home'
        # navigate back to the "Home" page
        home_page = leadership_page.select_page_from_top_menu(id)
        home_page.save_screenshot('home page loaded again')
        assert driver.title == home_page.title

    @pytest.mark.parametrize('scenario',
                            [
                                ['How It Works', 'Solution Providers', 'Leadership'],
                                ['Why Arctic Wolf', 'Solutions', 'How It Works'],
                                ['Resources', 'How It Works', 'Why Arctic Wolf'],
                                ['Solution Providers', 'Leadership', 'Solutions'],
                                ['Leadership', 'Why Arctic Wolf', 'Resources'],
                            ],
                            ids=['scenario01', 'scenario02', 'scenario03',
                                 'scenario04', 'scenario05']
    )
    def test_dynamic_navigation(self, driver, arcticwolf, scenario):
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
        page = boot_page.start_with('arcticwolf home page')
        page.save_screenshot('home loaded')

        for destination in scenario:
            logger.info(f"\nnavigating to {destination} page")
            page = page.select_page_from_top_menu(destination)
            page.save_screenshot(f"{destination.lower()} page loaded")
