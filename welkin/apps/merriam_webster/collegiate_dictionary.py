import logging

from welkin.apps.merriam_webster import base_endpoint
from welkin.framework.utils import plog


logger = logging.getLogger(__name__)


class CollegiateDictionaryEndpoint(base_endpoint.BaseEndpoint):

    def __init__(self, key):
        """
            The Collegiate Dictionary has just one endpoint, which takes two
            parameters:
                1. the word to look up
                2. the API key

            Instantiate the endpoint with the API key.THis has to be passed
            in the URL, and not through the headers.

            See reference: https://dictionaryapi.com/products/json

            :param key: str, API key
            :return: None
        """
        self.name = 'dictionary'
        self.api_key = key
        self.url_key_phrase = f"?key={self.api_key}"

        logger.info(f"{self.name} endpoint object created.")

    def get_word(self, word):
        """
            Grab the information for one word as specified by the
            word itself.

            :param word: str, word to look up
            :return res: Requests response object
        """
        url = self.base_url + word + self.url_key_phrase
        res = self.get(url, headers=self.headers)
        logger.info(f"res: {res.text}")
        return res
