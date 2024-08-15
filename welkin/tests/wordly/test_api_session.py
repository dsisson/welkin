import pytest
import logging

from welkin.framework import utils
from welkin.apps.wordly.api.api import SessionsEndpoint

logger = logging.getLogger(__name__)

TIMESTAMP = pytest.custom_namespace['timestamp']


@pytest.mark.api
class WordlyApiSessionsTests(object):
    """
        In these tests, the `wordly_api` fixture calls return the PI KEY.
    """

    def test_get_sessions(self, wordly_api):
        # disambiguation
        api_key = wordly_api

        # instantiate the API instance with the API key
        api = SessionsEndpoint(api_key)

        # get the glossaries
        res = api.get_sessions()

        # test point: verify the correct response for a correct api call
        assert res.status_code == 200

        # get the json payload so we can make some checks
        payload = res.json()
        logger.info(utils.plog(payload))

        # test point: verify that the json schema is correct
        # using an extremely simplified example
        assert api.validate_schema(res.json(), verbose=True)

    @pytest.mark.parametrize('query_args',
    [
        {'page': 1},
        {'page': 1, 'limit': 10},
        {'page': 2, 'limit': 20, 'search': 'foo'},
    ],
    ids=['p=1', 'p=1&l=10', 'p=2&l=20&s=foo'])
    def test_get_sessions_with_querystring(self, wordly_api, query_args):
        # disambiguation
        api_key = wordly_api

        # instantiate the API instance with the API key
        api = SessionsEndpoint(api_key)

        # get the glossaries, using the parametrized query args
        res = api.get_sessions(**query_args)

        # test point: verify the correct response for a correct api call
        assert res.status_code == 200

        # get the json payload so we can make some checks
        payload = res.json()
        logger.info(utils.plog(payload))

        # test point: verify that the json schema is correct
        # using an extremely simplified example
        assert api.validate_schema(res.json(), verbose=True)

    def test_create_session(self, wordly_api):
        # disambiguation
        api_key = wordly_api

        # instantiate the API instance with the API key
        api = SessionsEndpoint(api_key)

        # set up the payload
        data = {
            "title": f"Ethics Conference {TIMESTAMP}",
            "estimatedDuration": 10,
            "languageCode": "en"
        }
        res = api.create_session(data)

        # test point: verify the correct response for a correct api call
        assert res.status_code == 200

        # get the json payload so we can make some checks
        payload = res.json()
        logger.info(utils.plog(payload))

