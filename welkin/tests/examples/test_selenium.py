import pytest
import logging
import time

logger = logging.getLogger(__name__)


@pytest.mark.example
class ExampleSeleniumTests(object):

    @pytest.mark.selenium
    def test_google(self, init, driver):
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

    @pytest.mark.selenium
    def test_google_typo(self, init, driver):
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
