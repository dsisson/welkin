import pytest
import logging

from welkin.framework import utils
from welkin.apps.wordly.api.api import GlossariesEndpoint

logger = logging.getLogger(__name__)

TIMESTAMP = pytest.custom_namespace['timestamp']


@pytest.mark.api
class WordlyApiGlossaryTests(object):
    """
        In these tests, the `wordly_api` fixture calls return the PI KEY.
    """

    def test_get_glossaries(self, wordly_api):
        # disambiguation
        api_key = wordly_api

        # instantiate the API instance with the API key
        api = GlossariesEndpoint(api_key)

        # get the glossaries
        res = api.get_glossaries()

        # test point: verify the correct response for a correct api call
        assert res.status_code == 200

        # get the json payload so we can make some checks
        payload = res.json()
        logger.info(utils.plog(payload))

        # test point: verify that the json schema is correct
        # using an extremely simplified example
        assert api.validate_schema(res.json(), verbose=True)

    def test_create_glossary(self, wordly_api):
        # disambiguation
        api_key = wordly_api

        # instantiate the API instance with the API key
        api = GlossariesEndpoint(api_key)

        # set up the payload
        data = {
            "title": f"Example Ethics Glossary {TIMESTAMP}",
            "sections": [
                {
                    "languageCode": "en",
                    "phrases": ["deontological"],
                    "blockedPhrases": ["hellfire"],
                    "substitutedPhrases": {"academic": "real"}
                }
            ]
        }
        res = api.create_glossary(data)

        # test point: verify the correct response for a correct api call
        assert res.status_code == 200

        # get the json payload so we can make some checks
        payload = res.json()
        logger.info(utils.plog(payload))
