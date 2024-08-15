import pytest
import logging

from welkin.framework import utils
from welkin.apps.wordly.api.api import GlossariesEndpoint
from welkin.apps.wordly.data.errors import errors_model

logger = logging.getLogger(__name__)


@pytest.mark.api
class WordlyApiErrorTests(object):
    """
        In these tests, the `wordly_api` fixture calls return the API KEY.
    """

    def test_fail_auth_without_auth_kvpair(self, wordly_api):
        # disambiguation
        api_key = wordly_api

        expected_status = 401
        expected_error = 5003

        # instantiate the API instance with the API key
        api = GlossariesEndpoint(api_key)

        # now delete that auth k/v pair from the headers to force auth errors
        api._delete_authorization_token()

        # attempt to get the glossaries
        res = api.get_glossaries()

        # test point: auth should fail
        assert res.status_code == expected_status

        # get the json payload so we can make some checks
        payload = res.json()

        # test point: verify the correct error message for a failed auth
        assert payload == errors_model[expected_error]

    def test_fail_auth_with_bad_apikey(self, wordly_api):
        # disambiguation
        api_key = wordly_api

        expected_status = 401
        expected_error = 5003

        # swap the last char in the key to make it invalid
        api_key = api_key[:-1] + 'x'

        # instantiate the API instance with the API key
        api = GlossariesEndpoint(api_key)

        # attempt to get the glossaries
        res = api.get_glossaries()

        # test point: auth should fail
        assert res.status_code == expected_status

        # get the json payload so we can make some checks
        payload = res.json()

        # test point: verify the correct error message for a failed auth
        assert payload == errors_model[expected_error]



