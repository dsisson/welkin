import logging
import requests

from welkin.framework.exceptions import UnexpectedStatusCodeException
from welkin.framework.exceptions import JsonPayloadException
from welkin.framework.utils import plog


logger = logging.getLogger(__name__)


class GenderEndpoint(object):
    """
        Common ancestor for all endpoints.
    """
    base_url = 'https://api.genderize.io/'

    def __init__(self):
        """
            Initialize an endpoint object for testing.

            :return: None
        """
        self.expected_keys = [
                                'name',
                                'gender',
                                'probability',
                                'count'
                              ]
        self.expected_keys.sort()
        logger.info('Genderize endpoint object created.')

    def add_expected_key(self, new_key):
        """
            Based on optional parameters, add a key to the set of expected keys.

            :param new_key: str, key name
            :return: None
        """
        self.expected_keys.append(new_key)
        self.expected_keys.sort()
        logger.info('Added new key "%s" to the expected keys.')

    def get(self, ex=200, verbose=False, **kwargs):
        """
            Return the specified object for the specified API parameters. These are:
                `name`: str name or list of str names
                `country_id': str id for country (http://en.wikipedia.org/wiki/ISO_3166-1_alpha-2)
                `language_id`: str id for language (http://en.wikipedia.org/wiki/List_of_ISO_639-1_codes)

            :param ex: int, expected status code for the POST, defaults to a good 200.
                            Pass in an alternate code if testing error handling.
            :param verbose: bool, determines whether to output additional logging; defaults to False
            :param kwargs: dict of key-value pairs of additional parameters to be added to the url
            :return res: Requests response object
        """
        if verbose:
            logger.info('kwargs: %s' % kwargs)
            logger.info('url = %s' % self.base_url)
        res = requests.get(self.base_url, params=kwargs)
        logger.info('requested URL: "%s".' % res.url)

        if not res.status_code == ex:
            logger.error('Error: expected status code "%s" but got "%s".'
                         % (ex, res.status_code))
            logger.error(res.content)
            logger.info(res.headers)
            raise UnexpectedStatusCodeException(response=res)

        try:
            logger.info('%s genderize API requests remaining for this time period.'
                        % res.headers['X-Rate-Limit-Remaining'])
        except KeyError:
            logger.info('headers = %s' % plog(res.headers))

        if 'country_id' in res.json():
            self.add_expected_key('country_id')
        if 'language_id' in res.json():
            self.add_expected_key('language_id')

        return res

    def got_gender(self, response, expected_gender):
        """
            Verify that the api call returned an assigned gender value.

            :param response:
            :param expected_gender: str, expected gender
            :return: bool, False if gender is null, else True
        """
        try:
            if response.json()['gender'] == expected_gender:
                return True
            else:
                return False
        except KeyError:
            raise JsonPayloadException('Json does\'t contain the "gender" key.')

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


