import logging
from requests.exceptions import JSONDecodeError

from welkin.apps.root_endpoint import RootEndpoint
from welkin.framework import utils

logger = logging.getLogger(__name__)


class BaseEndpoint(RootEndpoint):

    base_url = 'https://census-toy.nceng.net/prod'

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

class ToyCensusEndpoint(BaseEndpoint):

    expected_keys = ['name', 'value']

    def __init__(self):
        self.name = 'toy census endpoint'
        self.endpoint = '/toy-census'
        self.endpoint_url = self.base_url + self.endpoint
        self.expected_keys.sort()
        logger.info(self.template_load % self.name)

    def get_count(self, users, action_type, top=None, expect_status=200,
                  expect_errors=False, verbose=True, **kwargs):
        """
            For the supplied list of users, request a count for the
            specified `action_type`.

            This endpoint returns a list of the values found by the
            `action_type` and counts.

            :param users: list of dicts, 1 or more users (randomuser.me format)
            :param action_type: str enum, [CountByGender, CountByCountry, or
                                            CountPasswordComplexity]
            :param top: int, if > 0, set the max number of results counted
            :param expect_status: int enum, the expected server status in response
            :param expect_errors: Bool, whether to expect errors
            :param verbose: Bool, whether to output additional logging information
            :param kwargs: dict of key-value pairs of additional parameters
            :return res: Requests response object
        """
        url = self.endpoint_url
        logger.info(f"\nkwargs:\n{utils.plog(kwargs)}")
        logger.info(f"\nusers:\n{utils.plog(users)}")

        # assemble payload
        payload = {
            'actionType': action_type,
            'users': None
        }

        # top is optional
        if not top == None: # not pythonic, but done this way purposely
            payload['top'] = top

        # add in the users
        payload['users'] = users
        logger.info(f"\npayload:\n{utils.plog(payload)}")

        # pass to the base endpoints *requests* wrapper
        res = self.post(url,
                        expect_status=expect_status,
                        expect_errors=expect_errors,
                        verbose=verbose,
                        **payload)

        logger.info('\nResponse status code is "%s:".' % res.status_code)
        if verbose:
            try:
                logger.info('\nResponse json: \n%s' % utils.plog(res.json()))
            except JSONDecodeError:
                logger.error('\ntrapped JSONDecodeError')

        return res
