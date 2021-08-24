import logging
import requests

from welkin.apps.root_endpoint import RootEndpoint
from welkin.framework.exceptions import UnexpectedStatusCodeException
from welkin.framework.exceptions import JsonPayloadException
from welkin.framework.utils import plog


logger = logging.getLogger(__name__)


class BaseEndpoint(RootEndpoint):
    """
        Common ancestor for all endpoints.
    """
    base_url = 'http://www.colourlovers.com/api/'

    # the header to be used for all requests
    headers = {'Content-Type': 'application/json'}
