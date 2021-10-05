import logging

from welkin.apps.root_endpoint import RootEndpoint
from welkin.framework import utils

logger = logging.getLogger(__name__)


class BaseEndpoint(RootEndpoint):

    base_url = 'https://icanhazdadjoke.com'

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }


class SearchEndpoint(BaseEndpoint):

    expected_keys = [
        'current_page',
        'limit',
        'next_page',
        'previous_page',
        'results',
        'search_term',
        'status',
        'total_jokes',
        'total_pages'
    ]

    schema = {
        'current_page': {'type': 'integer'},
        'limit': {'type': 'integer'},
        'next_page': {'type': 'integer'},
        'previous_page': {'type': 'integer'},
        'results': {'type': 'list'},
        'search_term': {'type': 'string'},
        'status': {'type': 'integer'},
        'total_jokes': {'type': 'integer'},
        'total_pages': {'type': 'integer'}
    }

    def __init__(self):
        self.name = 'dad jokes search'
        self.endpoint = '/search'
        self.endpoint_url = self.base_url + self.endpoint
        self.expected_keys.sort()
        logger.info(self.template_load % self.name)

    def search_for_joke(self, terms, expect_status=200, verbose=False):
        """

            :param terms:
            :param expect_status:
            :param verbose:
            :return:
        """
        url = f"{self.endpoint_url}?term={terms}"
        # pass to the base endpoints *requests* wrapper
        res = self.get(url, expect_status=expect_status)

        logger.info(f"Response status code is '{res.status_code}'")
        if verbose:
            logger.info(f"\nResponse json:\n{utils.plog(res.json())}")
        return res
