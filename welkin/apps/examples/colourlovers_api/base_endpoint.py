import logging

from welkin.apps.root_endpoint import RootEndpoint


logger = logging.getLogger(__name__)


class BaseEndpoint(RootEndpoint):
    """
        Common ancestor for all endpoints.
    """
    base_url = 'http://www.colourlovers.com/api/'

    # the header to be used for all requests
    headers = {'Content-Type': 'application/json'}
