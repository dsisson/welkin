import pytest
import logging
import json
import time

from welkin.framework import utils
from welkin.apps.examples.dadjokes_api.api import SearchEndpoint

logger = logging.getLogger(__name__)


@pytest.mark.example
@pytest.mark.api
class DadJokesTests(object):

    def test_search_for_joke(self, dadjokes):
        terms = 'bicycle'
        api = SearchEndpoint()
        res = api.search_for_joke(terms, verbose=True)

        # test point: verify that the json keys are correct
        # using the older keys expected_keys approach
        assert api.verify_keys_in_response(res.json().keys(), verbose=True)

        # test point: verify that the json schema is correct
        # using the new schema validator approach
        assert api.validate_schema(res.json(), verbose=True)
