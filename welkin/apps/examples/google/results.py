import logging
from welkin.apps.examples.google.base_page import PageObject
from welkin.framework.exceptions import PageIdentityException
from welkin.framework.exceptions import GoogleResultsCountException
from welkin.framework import utils

logger = logging.getLogger(__name__)


class SearchResultsPage(PageObject):

    sel_results_summary = 'topabar'
    sel_original_query = 'a.spell_orig'
    sel_corrected_query = 'a.spell'
    sel_results_list = 'div.g'
    sel_related_searches = 'div#brs a'
    sel_page_links = 'table#nav a'

    def __init__(self, driver):
        self.driver = driver
        logger.info('Instantiated Google search results PageObject.')

    def get_results_structure(self):
        """
            Grab some elements and content from the search results page, to be used in validating
            structure and content.

            :return checkpoints: dict, data describing some structural aspects of the results page
        """
        checkpoints = {}
        checkpoints['results summary'] = self._extract_results_summary()
        checkpoints['original_query'] = self._extract_original_query()
        checkpoints['corrected_query'] = self._extract_corrected_query()
        checkpoints['results_list'] = self._extract_results_list()
        checkpoints['related_searches'] = self._extract_related_searches()
        checkpoints['page_links'] = self._extract_pagination()
        logger.info('checkpoint = \n%s' % utils.plog(checkpoints))
        return checkpoints

    def _extract_results_summary(self):
        """
            Pull a results count out of the results summary.

            :return count: int, the number of search results items
        """
        raw_text = self.driver.find_element_by_id(self.sel_results_summary).text
        assumed_count = raw_text.split(' ')[1]
        try:
            count = int(assumed_count.replace(',', ''))
        except ValueError:
            msg = 'FAIL: expected the value "%s" to be a number; full result: %s%.' % (assumed_count, raw_text)
            logger.error(msg)
            raise GoogleResultsCountException(msg)

        return count

    def _extract_original_query(self):
        """
            Pull out the query as originally supplied, without spelling corrections.

            :return: False if not found, else str original_query
        """
        original_query = self.driver.find_element_by_css_selector(self.sel_original_query).text
        logger.info('Original query as displayed on result page: "%s".' % original_query)
        if original_query == '':
            return False
        else:
            return original_query

    def _extract_corrected_query(self):
        """
            Pull out the spelling-corrected query.

            :return: False if not found, else str original_query
        """
        corrected_query = self.driver.find_element_by_css_selector(self.sel_corrected_query).text
        logger.info('Corrected query as displayed on result page: "%s".' % corrected_query)
        if corrected_query == '':
            return False
        else:
            return corrected_query

    def _extract_results_list(self):
        """
            Pull out the document titles, as well as the highlighted query string matches from the
            displayed excerpts.

            :return results_list: list of tuples (title + list of string matches) for each result
        """
        results_list = []
        raw_results = self.driver.find_elements_by_css_selector(self.sel_results_list)
        for item in raw_results:
            title = item.find_element_by_tag_name('h3')
            matches = item.find_elements_by_tag_name('em')
            results_list.append((title, [match.text for match in matches]))
        logger.info('Search results item titles: %s' % [item[0].text for item in results_list])
        return results_list

    def _extract_related_searches(self):
        """
            Pull out the set of related searches.

            :return related_search_links: list of link webelements
        """
        related_search_links = self.driver.find_elements_by_css_selector(self.sel_related_searches)
        logger.info('Related search queries: %s' % [item.text for item in related_search_links])
        return related_search_links

    def _extract_pagination(self):
        """
            Pull out the set of pagination links.

            :return pagination_links: list of link webelements
        """
        pagination_links = self.driver.find_elements_by_css_selector(self.sel_page_links)
        return pagination_links
