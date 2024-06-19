import pytest
import logging

from welkin.framework import utils
from welkin.apps.examples.data_dot_gov import api
logger = logging.getLogger(__name__)


@pytest.mark.example
@pytest.mark.api
class ExampleDataDotGovTests(object):

    def test_crashes_list(self, data_dot_gov):
        # disambiguate
        api_key = data_dot_gov

        # instantiate the endpoint
        crashes_endpoint = api.VehicleCrashesEndpoint(api_key)

        # make the request
        res = crashes_endpoint.get_vehicle_crashes()
        assert res.status_code == 200
        logger.info(f"\nresults json:\n{utils.plog(res.json)}\n")

        # test point: verify that the json schema is correct
        # using the new schema validator approach
        assert crashes_endpoint.validate_schema(res.json()[0], verbose=True)


    @pytest.mark.xfail(reason="API doesn't require auth.")
    def test_crashes_no_key(self, data_dot_gov):
        # disambiguate
        api_key = data_dot_gov

        # instantiate the endpoint
        crashes_endpoint = api.VehicleCrashesEndpoint(api_key)

        # delete api key from headers, because we want to force an auth error
        headers = crashes_endpoint.delete_key_from_headers(crashes_endpoint.headers,
                                                           'X-Api-Key')

        # make the request
        res = crashes_endpoint.get_vehicle_crashes(headers=headers)
        assert res.status_code == 403
        logger.info(f"\nresults json:\n{utils.plog(res.json)}\n")

