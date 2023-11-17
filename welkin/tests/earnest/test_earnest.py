import pytest
import logging

from selenium.common.exceptions import ElementClickInterceptedException
from welkin.apps.earnest.noauth import pages

logger = logging.getLogger(__name__)


@pytest.mark.example
@pytest.mark.selenium
class EarnestTests(object):
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

    def test_linear_navigation(self, driver, earnest):
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

        id = 'Student Loans'
        student_loans_page = home_page.select_page_from_top_menu(id)
        student_loans_page.save_screenshot(f"{id.lower()} page loaded")

        id = 'Parent Loans'
        parent_loans_page = student_loans_page.select_page_from_top_menu(id)
        parent_loans_page.save_screenshot(f"{id.lower()} page loaded")

        id = 'Resources'
        resources_page = parent_loans_page.select_page_from_top_menu(id)
        resources_page.save_screenshot(f"{id.lower()} page loaded")

        id = 'Debt To Income Ratio'
        calculator_page = resources_page.select_page_from_top_menu(id)
        calculator_page.save_screenshot(f"{id.lower()} page loaded")

        id = 'Refinance Student Loans'
        refinance_page = calculator_page.select_page_from_top_menu(id)
        refinance_page.save_screenshot(f"{id.lower()} page loaded")

        id = 'Student Loan Manager'
        student_loan_manager_page = refinance_page.select_page_from_top_menu(id)
        student_loan_manager_page.save_screenshot(f"{id.lower()} page loaded")

        # navigate back to the "Home" page
        home_page = student_loan_manager_page.select_page_from_top_menu('Home')
        home_page.save_screenshot('home page loaded again')

    @pytest.mark.parametrize('scenario',
                            [
                                ['Student Loans', 'Resources', 'Parent Loans'],
                                ['Student Loan Manager', 'Student Loans',
                                 'Debt To Income Ratio'],
                                ['Refinance Student Loans', 'Home', 'Student Loans'],
                                ['Refinance Student Loans', 'Parent Loans', 'Resources'],
                                ['Debt To Income Ratio', 'Student Loan Manager', 'Home'],
                            ],
                            ids=['scenario01', 'scenario02', 'scenario03',
                                 'scenario04', 'scenario05']
    )
    def test_dynamic_navigation(self, driver, earnest, scenario):
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