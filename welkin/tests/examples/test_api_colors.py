import pytest
import logging
import time

from welkin.framework import utils
from welkin.apps.examples.colourlovers_api import color
from welkin.apps.examples.colourlovers_api import colors
from welkin.apps.examples.data import color_data

logger = logging.getLogger(__name__)


@pytest.mark.example
@pytest.mark.api
class ExampleColourLovers(object):
#class ExampleColourLoversTests(object):

    # setup: create instances of each endpoint, as class attributes of this test class
    color_endpoint = color.ColorEndpoint()
    colors_endpoint = colors.ColorsEndpoint()

    def test_get_color(self, colourlovers):
        """
            Simple test for the "color" endpoint, using hardcoded data.

            :return: None
        """

        # setup: make API request
        data = '000000'
        res = self.color_endpoint.get_color(data)

        # test point: verify the correct response for a correct api call
        assert res.status_code == 200
        logger.info(utils.plog(res.json()))

        # test point: verify that we get back the same hex that we requested
        assert res.json()[0]['hex'] == data

        # test point: verify that the json keys are correct
        assert self.color_endpoint.verify_keys_in_response(res.json()[0].keys())

    def test_get_colors(self, colourlovers):
        """
            Simple test for the "colors" endpoint, using no data. This just
            looks at the structure of the returned json.

            :return: None
        """
        # setup: make API request
        res = self.colors_endpoint.get_colors()

        # test point: verify the correct response for a correct api call
        assert res.status_code == 200
        logger.info(utils.plog(res.json()))

        # test point: verify that the json keys are correct
        assert self.color_endpoint.verify_keys_in_response(res.json()[0].keys())

    @pytest.mark.parametrize('colors_data', color_data, ids=[c[1] for c in color_data])
    def test_colordata(self, colourlovers, colors_data):
        """
            This is a parametrized test case using a data source consisting of a list of lists.
            Pytest will iterate over the data model and call this test method once for each top
            level item in that data model. For each call, we get a list consisting of a color
            name, its hex code, and its RGB values.

            The hex string is the second element in this data, so we get that by grabbing it by
            calling `colors_data[1]`. Then, we need to drop the prepended `#` by
            calling `colors_data[1][1:]`

            :param colors_data: list consisting of str color name, str hex code, str RGB values
            :return: None
        """
        logger.info('test data = "%s".' % colors_data)

        # setup: extract the hex string from the parametrized data input and make API request
        this_hex = colors_data[1][1:]
        res = self.color_endpoint.get_color(this_hex)

        # test point: verify the correct response for a correct api call
        assert res.status_code == 200
        logger.info(utils.plog(res.json()))

        # test point: verify that we get back the same hex that we requested
        assert res.json()[0]['hex'] == this_hex

        # test point: verify that the json keys are correct
        assert self.color_endpoint.verify_keys_in_response(res.json()[0].keys())

        # slow down the API calls so that we don't cause problems or exceed our welcome
        time.sleep(2)
