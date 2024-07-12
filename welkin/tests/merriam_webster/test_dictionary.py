import pytest
import logging
import time

from welkin.framework import utils
from welkin.apps.merriam_webster import collegiate_dictionary as mw

logger = logging.getLogger(__name__)


@pytest.mark.example
@pytest.mark.api
class CollegiateDictionaryTests(object):

    @pytest.mark.parametrize('words', [
        'run',
        'retreat',
        'run-of-the-mill',
        'fetching'
    ])
    def test_get_definition(self, merriam_webster, words):
        """
            Simple test for the word endpoint.

            Note that our tests are only for simple words that are not stemmed
            so much that they are unrecognizable. We are not testing for
            edge cases or for words that are not in the dictionary.

            :param merriam_webster: str, the API key
            :param words: str, the word to look up
            :return: None
        """
        # disambiguation
        api_key = merriam_webster
        word = words

        # instantiate the API instance with the API key
        api = mw.CollegiateDictionaryEndpoint(api_key)

        # get a definition
        res = api.get_word(word)

        # test point: verify the correct response for a correct api call
        assert res.status_code == 200

        # get the json payload so we can make some checks
        payload = res.json()
        logger.info(utils.plog(payload))

        # the searched-for word should be in the response
        id = payload[0]['meta']['id']  # just the first one
        check_point = id[:id.find(':')] if id.find(':') > 0 else id
        assert check_point == word

