import logging
import requests

from welkin.framework.exceptions import UnexpectedStatusCodeException
from welkin.framework.exceptions import JsonPayloadException
from welkin.framework.utils import plog


logger = logging.getLogger(__name__)


class BaseEndpoint(object):
    """
        Common ancestor for all endpoints.
    """
    base_url = 'http://www.colourlovers.com/api/'

    # the header to be used for all requests
    # json_header = {'Content-Type': 'application/json'}

    def get(self, url, ex=200, **kwargs):
        """
            Return the specified object for this specified UID .

            :param url: str, the interim url to be used for this API call; may be extended by params
            :param ex: int, expected status code for the POST, defaults to a good 201. Pass in an alternate code if
                            testing error handling.
            :param kwargs: dict of key-value pairs of additional parameters to be added to the url
            :return res: Requests response object
        """
        logger.info('kwargs: %s' % kwargs)
        res = requests.get(url, params=kwargs)
        logger.info('requested URL: "%s".' % res.url)

        if not res.status_code == 200:
            logger.error(res.status_code)
            logger.error(res.content)
            raise UnexpectedStatusCodeException(response=res)

        return res

    def verify_keys_in_response(self, response_keys):
        """
            Verify that the endpoint response contains the expected keys.

            :param response_keys: dict_keys, the keys from an instance of the response object json
            :return: True if keys are equal, else raise exception
        """
        # be strict about checking keys
        expected = self.expected_keys
        actual = list(response_keys)
        actual.sort()
        logger.debug('Comparing expected keys "%s" to\n          actual keys "%s".' % (expected, actual))

        if sorted(expected) == sorted(actual):
            logger.debug('Comparison results: Keys are equal.')
            return True
        else:
            logger.error('Comparison results: Keys are NOT equal.')
            logger.error('Expected keys:\n%s' % plog(expected))
            logger.error('Actual keys:\n%s' % plog(response_keys))
            raise JsonPayloadException('Actual keys don\'t match expected keys.')


