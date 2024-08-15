import pytest
import logging
import time

from welkin.framework import utils
from welkin.apps.wordly.api.api import GlossariesEndpoint
from welkin.apps.wordly.api.api import SessionsEndpoint
from welkin.apps.wordly.api.api import TranscriptionsEndpoint
from welkin.apps.wordly.data.transcriptions import downloadable_transcription as transcripts

logger = logging.getLogger(__name__)

TIMESTAMP = pytest.custom_namespace['timestamp']


@pytest.mark.api
class WordlyApiEndToEndTests(object):
    """
        In these tests, the `wordly_api` fixture calls return the API KEY.

        For the purposes of this test example, we pretend that the
        core Wordly customer scenario is:
        1. check to see if a specific glossary exists; if not, create it
        2. create a new session
        3. check for a specific transcription; if not, create it
        4. download the transcription
    """

    def test_wordly_scenario(self, wordly_api):
        # disambiguation
        api_key = wordly_api
        target_glossary = f"Example Ethics Glossary {TIMESTAMP}"
        target_transcription = f"taunt {TIMESTAMP}"

        # step 1a: does this already exist (it should not)

        api_glossaries = GlossariesEndpoint(api_key)
        # get the glossaries
        res = api_glossaries.get_glossaries()
        assert res.status_code == 200

        # look up our target
        glossaries = [g['title'] for g in res.json()['glossaries']]
        logger.info(f"\nexisting glossaries: {glossaries}")

        if target_glossary not in glossaries:
            # step 1b: create the glossary
            data = {
                "title": target_glossary,
                "sections": [
                    {
                        "languageCode": "en",
                        "phrases": ["deontological"],
                        "blockedPhrases": ["hellfire"],
                        "substitutedPhrases": {"academic": "real"}
                    }
                ]
            }
            res = api_glossaries.create_glossary(data)
            assert res.status_code == 200

        # step 2: create a new session
        api_sessions = SessionsEndpoint(api_key)

        # set up the payload
        data = {
            "title": f"Ethics Conference {TIMESTAMP}",
            "estimatedDuration": 10,
            "languageCode": "en"
        }

        res = api_sessions.create_session(data)
        assert res.status_code == 200

        # step 3a: does this transcription already exist (it should not)
        api_transcriptions = TranscriptionsEndpoint(api_key)
        res = api_transcriptions.get_transcriptions()
        assert res.status_code == 200

        # look up our target
        transcripts = [t['name'] for t in res.json()]
        logger.info(f"\nexisting transcriptions: {glossaries}")

        transcription_id = None
        if target_transcription not in transcripts:
            # step 3b: create the transcription
            # set up the payload
            data = {
                "name": f"taunt {TIMESTAMP}",
                "url": "https://www2.cs.uic.edu/~i101/SoundFiles/taunt.wav",
                "sourceLanguageCode": "en",
                "targetLanguageCodes": ["es"],
            }

            res = api_transcriptions.create_transcription(data)
            assert res.status_code == 200
            transcription_id = res.json()['id']

        # absolutely do NOT put a hardcoded sleep here ;)
        time.sleep(10)

        # step 4: download the transcription
        query_args = {'language_codes': ['es'], 'formats': ['txt']}
        res = api_transcriptions.download_transcription(transcription_id, **query_args)
        assert res.status_code == 200
        logger.info(f"transcription downloaded: {res.text}")

