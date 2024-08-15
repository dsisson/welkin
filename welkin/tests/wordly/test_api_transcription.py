import pytest
import logging

from welkin.framework import utils
from welkin.apps.wordly.api.api import TranscriptionsEndpoint
from welkin.apps.wordly.data.transcriptions import downloadable_transcription as transcripts

logger = logging.getLogger(__name__)

TIMESTAMP = pytest.custom_namespace['timestamp']


@pytest.mark.api
class WordlyApiTranscriptionTests(object):
    """
        In these tests, the `wordly_api` fixture calls return the PI KEY.
    """

    def test_get_transcriptions(self, wordly_api):
        # disambiguation
        api_key = wordly_api

        # instantiate the API instance with the API key
        api = TranscriptionsEndpoint(api_key)

        # get the glossaries
        res = api.get_transcriptions()

        # test point: verify the correct response for a correct api call
        assert res.status_code == 200

        # get the json payload so we can make some checks
        payload = res.json()
        logger.info(utils.plog(payload))

        # test point: verify that the json schema is correct
        # using an extremely simplified example
        # assert api.validate_schema(res.json(), verbose=True)

    def test_create_transcription(self, wordly_api):
        # disambiguation
        api_key = wordly_api

        # instantiate the API instance with the API key
        api = TranscriptionsEndpoint(api_key)

        # set up the payload
        data = {
            "name": f"taunt {TIMESTAMP}",
            "url": "https://www2.cs.uic.edu/~i101/SoundFiles/taunt.wav",
            "sourceLanguageCode": "en",
            "targetLanguageCodes": ["es"],
        }
        res = api.create_transcription(data)

        # test point: verify the correct response for a correct api call
        assert res.status_code == 200

        # get the json payload so we can make some checks
        payload = res.json()
        logger.info(utils.plog(payload))

    @pytest.mark.parametrize('query_args',
    [
        {'language_codes': ['es'], 'formats': ['txt']},
    ],
    ids=['lc=es,f=txt'])
    def test_download_transcription(self, wordly_api, query_args):
        # disambiguation
        api_key = wordly_api

        # hardcoded for simplicity
        target_id = transcripts['taunt 240816-143228']['id']

        # instantiate the API instance with the API key
        api = TranscriptionsEndpoint(api_key)

        # get the glossaries, using hardcoded id but parametrized query args
        res = api.download_transcription(target_id, **query_args)

        # test point: verify the correct response for a correct api call
        assert res.status_code == 200

        # get the json payload so we can make some checks
        payload = res.json()
        logger.info(utils.plog(payload))

