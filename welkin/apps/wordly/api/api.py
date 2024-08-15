import logging

from welkin.apps.wordly.api import base_endpoint
from welkin.framework.utils import plog


logger = logging.getLogger(__name__)


class SessionsEndpoint(base_endpoint.BaseEndpoint):

    schema = {  # extremely simplified!
        'page': {'type': 'integer'},
        'limit': {'type': 'integer'},
        'total': {'type': 'integer'},
        'sessions': {'type': 'list'},
    }

    def __init__(self, key):
        self.name = 'sessions'
        self.api_key = key
        self._set_authorization_token()
        self.endpoint = '/sessions'
        self.endpoint_url = self.base_url + self.endpoint
        logger.info(f"{self.name} endpoint object created.")

    def get_sessions(self, **args):
        """
            Grab the list of sessions.

            :param args: dict, query params to control filtering/paging
            :return res: Requests response object
        """
        url = self.endpoint_url
        if args:
            logger.info(f"query string args: {args}")
            res = self.get(url, params=args)
        else:
            res = self.get(url)
        logger.info(f"res: {res.text}")
        return res

    def create_session(self, data):
        """
            Create a new session.

            :param data: dict, the session data
            :return res: Requests response object
        """
        logger.info(f"payload data: \n{plog(data)}")
        apiurl = self.endpoint_url
        res = self.post(apiurl, **data)
        logger.info(f"res: {res.text}")
        logger.info(f"request body: {res.request.body}")
        return res


class GlossariesEndpoint(base_endpoint.BaseEndpoint):

    schema = {  # extremely simplified!
        'page': {'type': 'integer'},
        'limit': {'type': 'integer'},
        'total': {'type': 'integer'},
        'glossaries': {'type': 'list'},
    }

    def __init__(self, key):
        self.name = 'glossaries'
        self.api_key = key
        self._set_authorization_token()
        self.endpoint = '/glossaries'
        self.endpoint_url = self.base_url + self.endpoint
        logger.info(f"{self.name} endpoint object created.")

    def get_glossaries(self):
        """
            Grab the list of glossaries.

            :return res: Requests response object
        """
        url = self.endpoint_url
        res = self.get(url)
        logger.info(f"res: {res.text}")
        return res

    def create_glossary(self, data):
        """
            Create a new glossary.

            Example payload:
            {
                "title": "Developer API",
                "sections": [
                    {
                        "languageCode": "en",
                        "phrases": [
                            "Dijkstra"
                        ],
                        "blockedPhrases": [
                            "darn"
                        ],
                        "substitutedPhrases": {
                            "hi": "hello",
                            "Sean": "Shawn"
                        }
                    }
                ]
            }

            :param data: dict, the glossary data
            :return res: Requests response object
        """
        logger.info(f"payload data: \n{plog(data)}")
        apiurl = self.endpoint_url
        res = self.post(apiurl, **data)
        logger.info(f"res: {res.text}")
        return res


class TranscriptionsEndpoint(base_endpoint.BaseEndpoint):

    def __init__(self, key):
        self.name = 'transcriptions'
        self.api_key = key
        self._set_authorization_token()
        self.endpoint = '/media/transcriptions'
        self.endpoint_url = self.base_url + self.endpoint
        logger.info(f"{self.name} endpoint object created.")

    def get_transcriptions(self):
        """
            Grab the list of transcriptions.

            :return res: Requests response object
        """
        url = self.endpoint_url
        res = self.get(url)
        logger.info(f"res: {res.text}")
        return res

    def create_transcription(self, data):
        """
            Create a new transcription for a media file.

            :return res: Requests response object
        """
        logger.info(f"payload data: \n{plog(data)}")
        apiurl = self.endpoint_url
        res = self.post(apiurl, **data)
        logger.info(f"res: {res.text}")
        logger.info(f"request body: {res.request.body}")
        return res

    def download_transcription(self, id, **args):
        """
            Download the transcription with id `id`.

            :param id: int, the transcription id
            :param args: dict, query params
            :return res: Requests response object
        """
        url = self.endpoint_url + f'/{id}'
        if args:
            logger.info(f"query string args: {args}")
            res = self.get(url, params=args)
        else:
            res = self.get(url)
        logger.info(f"res: {res.text}")
        return res
