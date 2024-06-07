import pytest
import logging

from welkin.apps.transfinder.base_page import PomBootPage

logger = logging.getLogger(__name__)


@pytest.mark.example
@pytest.mark.selenium
class TransfinderTests(object):
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

    def test_linear_navigation(self, driver, transfinder):
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
        home_page = boot_page.start_with('transfinder home page')
        home_page.save_screenshot('home loaded')
        assert driver.title == home_page.title

        id = 'Viewfinder'
        viewfinder_page = home_page.select_page_from_top_menu(id)
        viewfinder_page.save_screenshot(f"{id.lower()} page loaded")
        assert driver.title == viewfinder_page.title

        id = 'Tripfinder'
        tripfinder_page = viewfinder_page.select_page_from_top_menu(id)
        tripfinder_page.save_screenshot(f"{id.lower()} page loaded")
        assert driver.title == tripfinder_page.title

        id = 'Marketplace'
        marketplace_page = tripfinder_page.select_page_from_top_menu(id)
        marketplace_page.save_screenshot(f"{id.lower()} page loaded")
        assert driver.title == marketplace_page.title

        id = 'Professional Services'
        proservices_page = marketplace_page.select_page_from_top_menu(id)
        proservices_page.save_screenshot(f"{id.lower()} page loaded")
        assert driver.title == proservices_page.title

        id = 'Case Studies'
        case_studies_page = proservices_page.select_page_from_top_menu(id)
        case_studies_page.save_screenshot(f"{id.lower()} page loaded")
        assert driver.title == case_studies_page.title

        id = 'Company'
        company_page = case_studies_page.select_page_from_top_menu(id)
        company_page.save_screenshot(f"{id.lower()} page loaded")
        assert driver.title == company_page.title

        id = 'Home'
        # navigate back to the "Home" page
        home_page = company_page.select_page_from_top_menu(id)
        home_page.save_screenshot('home page loaded again')
        assert driver.title == home_page.title

    @pytest.mark.parametrize('scenario',
                            [
                                ['Tripfinder', 'Case Studies', 'Viewfinder'],
                                ['Marketplace', 'Company', 'Tripfinder'],
                                ['Professional Services', 'Viewfinder', 'Company'],
                                ['Case Studies', 'Marketplace', 'Professional Services'],
                                ['Company', 'Professional Services', 'Marketplace'],
                            ],
                            ids=['scenario01', 'scenario02', 'scenario03',
                                 'scenario04', 'scenario05']
    )
    def test_dynamic_navigation(self, driver, transfinder, scenario):
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
        page = boot_page.start_with('transfinder home page')
        page.save_screenshot('home loaded')

        for destination in scenario:
            logger.info(f"\nnavigating to {destination} page")
            page = page.select_page_from_top_menu(destination)
            page.save_screenshot(f"{destination.lower()} page loaded")
