import logging

from welkin.apps.root_endpoint import RootEndpoint


logger = logging.getLogger(__name__)


class BaseEndpoint(RootEndpoint):
    """
        Common ancestor for all endpoints.
    """
    base_url = 'https://dev-api.wordly.ai'

    # the header to be used for all requests
    headers = {
        'Content-Type': 'application/json',
        'x-wordly-api-version': '1.0'
    }

    def _set_authorization_token(self):
        """
            Add the `x-wordly-api-key` auth token header to this endpoint
            object's headers.

            :return: None
        """
        # the headers exist for this endpoint; add a new key-value pair
        self.headers['x-wordly-api-key'] = self.api_key

    def _delete_authorization_token(self):
        """
            Delete the `x-wordly-api-key` auth token header from this endpoint
            object's headers, if it exists.

            :return: None
        """
        try:
            del self.headers['x-wordly-api-key']
        except KeyError:
            # the header key doesn't exist, that's OK for our needs
            pass
