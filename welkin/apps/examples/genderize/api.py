import logging

from welkin.apps.root_endpoint import RootEndpoint
from welkin.framework.exceptions import JsonPayloadException
from welkin.framework.utils import plog


logger = logging.getLogger(__name__)


class GenderEndpoint(RootEndpoint):
    """
        Common ancestor for all endpoints.
    """
    base_url = 'https://api.genderize.io/'

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    schema = {
        'count': {'type': 'integer'},
        'gender': {'type': 'string'},
        'name': {'type': 'string'},
        'probability': {'type': 'float'}
    }

    def __init__(self):
        """
            Initialize an endpoint object for testing.

            :return: None
        """
        self.name = 'genderize get gender'
        self.endpoint_url = self.base_url
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

    def get_gender(self, names, expect_status=200, verbose=False):
        """

            :param names: list of str names
            :param expect_status:
            :param verbose:
            :return:
        """
        # convert list of names into a params dict
        if isinstance(names, list):
            querystring = f"?name[]={'&name[]='.join(names)}"
        else:
            querystring = f"?name={names}"
        if verbose:
            logger.info(f"\n----> querystring: {querystring}")

        url = f"{self.endpoint_url}{querystring}"
        res = self.get(url, expect_status=expect_status, verbose=True)

        logger.info(f"Response status code is '{res.status_code}'")
        if verbose:
            logger.info(f"\nResponse json:\n{plog(res.json())}")
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
