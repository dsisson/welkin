import logging

from welkin.apps.examples.colourlovers_api import base_endpoint
from welkin.framework.utils import plog


logger = logging.getLogger(__name__)


class ColorEndpoint(base_endpoint.BaseEndpoint):

    def __init__(self):
        """
        /color/ endpoint

        :return: None
        """
        self.name = 'color'
        self.endpoint = 'color/'
        self.endpoint_url = self.base_url + self.endpoint
        self.expected_keys = [
                                'apiUrl',
                                'badgeUrl',
                                'dateCreated',
                                'description',
                                'hex',
                                'hsv',
                                'id',
                                'imageUrl',
                                'numComments',
                                'numHearts',
                                'numViews',
                                'numVotes',
                                'rank',
                                'rgb',
                                'title',
                                'url',
                                'userName'
                              ]
        self.expected_keys.sort()

        logger.info('Color endpoint object created.')

    def get_color(self, hex, format='json', expect_status=200, verbose=True, **kwargs):
        """
            Grab the information for one color as specified by the
            color's hexadecimal code.

            This endpoint returns a list of json dicts, even though there
            is only one color returned. The calling code will have to
            handle this list; for example:

            >>> res = self.color_endpoint.get_color('000000')
            >>> assert res.json()[0]['hex'] == '000000'

            :param hex: str, 6-character hex for color
            :param format: str, either `xml` or `json`; defaults to `json`
            :param verbose: Bool, whether to output additional logging information
            :param kwargs: dict of key-value pairs of additional parameters
            :return res: Requests response object
        """
        kwargs['format'] = format
        url = self.endpoint_url + hex
        logger.info('hex: "%s"; url will be "%s".' % (hex, url))
        logger.info('kwargs = %s' % kwargs)

        # pass to the base endpoints *requests* wrapper
        res = self.get(url, expect_status=expect_status, **kwargs)

        logger.info('Response status code is "%s:".' % res.status_code)
        if verbose:
            logger.info('Response json: \n%s' % plog(res.json()))
        return res
