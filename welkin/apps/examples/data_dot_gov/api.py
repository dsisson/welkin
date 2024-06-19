import logging

from welkin.apps.root_endpoint import RootEndpoint
from welkin.framework import utils

logger = logging.getLogger(__name__)


class BaseEndpoint(RootEndpoint):

    # base_url = 'https://developer.nrel.gov/api'

    def set_headers(self, api_key):
        """
            Set the headers for the request.

            :param api_key: str, API key passed through the CLI --dotgov_key arg
            :return headers: dict,
        """
        headers = {
            # 'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-Api-Key': api_key
        }
        return headers

    def delete_key_from_headers(self, headers, key):
        """
            Set the headers for the request.

            :param headers: dict, headers to be modified
            :param key: str, header key to be deleted
            :return headers: dict, updated headers
        """
        if key in headers:
            logger.info(f"/nkey '{key}' found in headers; deleting it.")
            del headers[key]
            logger.info(f"/nupdated headers: {utils.plog(headers)}")
            return headers


class VehicleCrashesEndpoint(BaseEndpoint):

    # documentation: https://dev.socrata.com/foundry/data.cityofnewyork.us/h9gi-nx95
    base_url = 'https://data.cityofnewyork.us/resource/h9gi-nx95.json'

    schema = {
        'collision_id': {'type': 'string'},  # 'integer'
        'contributing_factor_vehicle_1': {'type': 'string'},
        'contributing_factor_vehicle_2': {'type': 'string'},
        'crash_date': {'type': 'string'},  # 'datetime'
        'crash_time': {'type': 'string'},  # 'datetime'
        'number_of_cyclist_injured': {'type': 'string'},  # 'integer'
        'number_of_cyclist_killed': {'type': 'string'},  # 'integer'
        'number_of_motorist_injured': {'type': 'string'},  # 'integer'
        'number_of_motorist_killed': {'type': 'string'},  # 'integer'
        'number_of_pedestrians_injured': {'type': 'string'},  # 'integer'
        'number_of_pedestrians_killed': {'type': 'string'},  # 'integer'
        'number_of_persons_injured': {'type': 'string'},  # 'integer'
        'number_of_persons_killed': {'type': 'string'},  # 'integer'
        'off_street_name': {'type': 'string'},
        'on_street_name': {'type': 'string'},
        'vehicle_type_code1': {'type': 'string'},
        'vehicle_type_code2': {'type': 'string'}
    }


    def __init__(self, api_key):
        self.name = 'NYC vehicle crashes'
        self.api_key = api_key
        self.headers = self.set_headers(api_key)
        logger.info(self.template_load % self.name)

    def get_vehicle_crashes(self, headers=None,
                            expect_status=200, verbose=False):
        """
        Get vehicle crashes for a state and year.

        :param state: the state to get crashes for
        :param year: the year to get crashes for
        :param expect_status: the expected status code
        :param verbose: whether to print debug info
        :return: the response
        """
        if headers is None:
            headers = self.headers
        response = self.get(self.base_url, headers=headers, expect_status=expect_status, verbose=verbose)
        return response

