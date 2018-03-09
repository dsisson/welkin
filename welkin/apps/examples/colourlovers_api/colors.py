import logging

from welkin.apps.examples.colourlovers_api import base_endpoint
from welkin.framework.exceptions import UnexpectedStatusCodeException
from welkin.framework.utils import plog


logger = logging.getLogger(__name__)


class ColorsEndpoint(base_endpoint.BaseEndpoint):

    def __init__(self):
        """
        /colors/ endpoint

        :return: None
        """
        self.name = 'colors'
        self.endpoint = 'colors/'
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

        logger.info('Colors endpoint object created.')

    def get_colors(self, format='json', verbose=True, **kwargs):
        """
            Grab the first n-results for the parameters passed to the colors endpoint.


            This endpoint returns a list of json dicts, even though their is only one color returned.
            The calling code will have to handle that. for example:

            >>> res = self.colors_endpoint.get_colors('000000')
            >>> assert res.json()[0]['hex'] == '000000'

            :param format: str, either `xml` or `json`; defaults to `json`
            :param verbose: Bool, whether to output additional logging information
            :param kwargs: dict of key-value pairs of additional parameters
            :return res: Request response object with a json list of dicts
        """
        kwargs['format'] = format
        logger.info('kwargs = %s' % kwargs)

        # pass to the base endpoints *requests* wrapper
        res = self.get(self.endpoint_url, **kwargs)

        logger.info('Response status code is "%s:".' % res.status_code)
        if verbose:
            logger.info('Response json: \n%s' % plog(res.json()))
        return res
