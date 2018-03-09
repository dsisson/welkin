import pytest
import logging
import time

logger = logging.getLogger(__name__)


@pytest.mark.example
@pytest.mark.selenium
class ExampleSeleniumTests(object):
    """
        These selenium tests each call a selenium fixture that calls a fresh browser instance; that's
        an architectural decision, that every test starts fresh. You could just as easily use one browser
        session for *every* selenium test.

        This selenium fixture is scoped at the function level, and called by the test method as
        `driver'; that fixture is found on:
        welkin/tests/conftest.py::driver()

        pytest ficture documentation: https://docs.pytest.org/en/latest/fixture.html
    """
    def test_google_brittle(self):
        """
            Using a correctly-spelled query string, validate some structural test points on the search
            results page, but do everything the brittle way, with non-abstracted selenium code.
        """
        # selenium set up
        from selenium import webdriver
        from selenium.common.exceptions import NoSuchElementException
        driver = webdriver.Chrome()
        driver.implicitly_wait(10)  # default wait for 10 seconds
        logger.info('Starting driver.')

        # load home page
        driver.get('https://www.google.com')

        # verify that we are on the correct page
        # set expectations
        expected_title = 'Google'
        expected_domain = 'www.google.com'

        # actual results
        domain_from_url = driver.current_url.split('/')
        actual_title = driver.title
        actual_domain = domain_from_url[2]

        # validate expectations
        if not actual_title == expected_title and actual_domain == expected_domain:
            from welkin.framework.exceptions import PageIdentityException
            msg1 = 'FAIL: Google home page did NOT self-validate identity. '
            msg2 = 'Expected "%s" + "%s", got "%s" + "%s".' % \
                   (expected_title, expected_domain, actual_title, actual_domain)

            logger.error(msg1 + msg2)
            raise PageIdentityException(msg1 + msg2)

        # perform search
        search_input = driver.find_element_by_name('q')

        # pass in the search string
        search_input.send_keys('test case design in python')

        # submit the search
        search_input.submit()

        time.sleep(1)

        # we have a bunch of checkpoints that each require some setup

        # validate search results
        # 1. query should not be displayed on results list
        try:
            original_query = driver.find_element_by_css_selector('a.spell_orig').text
            assert original_query == '', 'FAIL: expected "", got "%s".' % original_query
        except NoSuchElementException:
            # not found, that's a good result
            pass
        logger.info('Assertion 1 passed.')

        # 2. there should be no spell-corrected query
        try:
            corrected_query = driver.find_element_by_css_selector('a.spell').text
            assert not corrected_query == '', 'FAIL: expected "", got "%s".' % corrected_query
        except NoSuchElementException:
            # not found, that's a good result
            pass
        logger.info('Assertion 2 passed.')

        # 3. there should be at least 10 results for this query on the first page
        results_list = []
        raw_results = driver.find_elements_by_css_selector('div.g')
        for item in raw_results:
            title = item.find_element_by_tag_name('h3')
            matches = item.find_elements_by_tag_name('em')
            results_list.append((title, [match.text for match in matches]))
        assert len(results_list) == 10, 'FAIL: expected 10 results, but got %d' % len(results_list)
        logger.info('Assertion 3 passed.')

        # 4. There should be related search suggestions
        related_search_links = driver.find_elements_by_css_selector('div#brs a')
        assert len(related_search_links) == 8, 'FAIL: expected 8 related links, but got %d' \
                                               % len(related_search_links)
        logger.info('Assertion 4 passed.')

        # 5. every result excerpt should display at least one keyword match from the query
        assert len(results_list[1]) >= 1, 'FAIL: no apparent matches in result excerpt: %s' \
                                                         % results_list[1]
        logger.info('Assertion 5 passed.')

        # clean up
        driver.quit()

    def test_google_abstracted(self, driver):
        """
            Using a correctly-spelled query string, validate some structural test points on the search
            results page.
        """
        query = 'test case design in python'

        # instantiate page object model for google.com
        from welkin.apps.examples.google.home import HomePage
        page = HomePage(driver)

        # load home page
        page.load()

        # verify that we are on the correct page
        assert page.verify_self()

        # perform search
        page = page.search_for(query)
        time.sleep(1)

        checkpoints = page.get_results_structure()

        # validate search results
        # 1. query should not be displayed on results list
        assert not checkpoints['original_query'], 'FAIL: expected False, got "%s".' % checkpoints['original_query']

        # 2. there should be no spell-corrected query
        assert not checkpoints['corrected_query'], 'FAIL: expected False, got "%s".' % checkpoints['corrected_query']

        # 3. there should be at least 10 results for this query on the first page
        assert len(checkpoints['results_list']) == 10, 'FAIL: expected 10 results, but got %d' \
                                                           % len(checkpoints['results_list'])

        # 4. There should be related search suggestions
        assert len(checkpoints['related_searches']) == 8, 'FAIL: expected 8 related links, but got %d' \
                                                           % len(checkpoints['related_searches'])

        # 5. every result excerpt should display at least one keyword match from the query
        assert len(checkpoints['results_list'][1]) >= 1, 'FAIL: no apparent matches in result excerpt: %s' \
                                                         % checkpoints['results_list'][1]

    def test_google_typo(self, driver):
        """
            Using query string with a mispelled word, validate some structural test points on the search
            results page.
        """
        query = 'test case deign in python'
        fixed_query = 'test case design in python'

        # instantiate page object model for google.com
        from welkin.apps.examples.google.home import HomePage
        page = HomePage(driver)

        # load home page
        page.load()

        # verify that we are on the correct page
        assert page.verify_self()

        # perform search
        page = page.search_for(query)
        time.sleep(1)

        checkpoints = page.get_results_structure()

        # validate search results
        assert checkpoints, checkpoints

        # validate search results
        # 1. query should be displayed on results list
        assert checkpoints['original_query'] == query, 'FAIL: expected "%s", got "%s".' \
                                                       % (query, checkpoints['original_query'])

        # 2. there should be a spell-corrected query
        assert checkpoints['corrected_query'] == fixed_query, 'FAIL: expected "%s", got "%s".'\
                                                              % (fixed_query, checkpoints['corrected_query'])

        # 3. there should be at least 10 results for this query on the first page
        assert len(checkpoints['results_list']) == 10, 'FAIL: expected 10 results, but got %d' \
                                                           % len(checkpoints['results_list'])

        # 4. There should be related search suggestions
        assert len(checkpoints['related_searches']) == 8, 'FAIL: expected 8 related links, but got %d' \
                                                           % len(checkpoints['related_searches'])

        # 5. every result excerpt should display at least one keyword match from the query
        assert len(checkpoints['results_list'][1]) >= 1, 'FAIL: no apparent matches in result excerpt: %s' \
                                                         % checkpoints['results_list'][1]

    def test_google_rgb_widget(self, driver):
        """

        :param driver:
        :return:
        """
        # instantiate page object model for google.com
        from welkin.apps.examples.google.home import HomePage
        page = HomePage(driver)

        # load home page
        page.load()

        # verify that we are on the correct page
        assert page.verify_self()
