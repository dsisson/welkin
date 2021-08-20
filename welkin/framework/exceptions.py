"""
    Custom Welkin exceptions, managed in one place.
"""
import logging

logger = logging.getLogger(__name__)


class JsonPayloadException(Exception):
    pass


class UnexpectedStatusCodeException(Exception):
    """
        Raise this exception when the server response code from an http request is not a success code.
        Capture the requests response object and make that available.

        # pass the response object to the exception
        >>> raise UnexpectedStatusCodeException(response=res)

        # then catch and introspect the exception's property
        >>> except UnexpectedStatusCodeException as e:
            ... print(e.response.status_code)
        400
    """
    def __init__(self, response):
        Exception.__init__(self, response)
        self.response = response


# ######################################
# page-object-focused exceptions
# ######################################
class PageLoadException(Exception):
    """
        Raise this exception when a page fails its load validations.
        Capture the errors and make them available.
    """
    def __init__(self, errors=None):
        Exception.__init__(self, errors)
        self.errors = errors


class PageUnloadException(Exception):
    """
        Raise this exception when a page fails its unload validation.
        Capture the errors and make them available.
    """
    def __init__(self, errors=None):
        Exception.__init__(self, errors)
        self.errors = errors


class PageIdentityException(Exception):
    """
        Raise this exception when a page fails its self validation of identity.
    """
    def __init__(self, errors=None):
        Exception.__init__(self, errors)
        self.errors = errors


class ControlInteractionException(Exception):
    """
        Raise this exception when an an interaction with a control
        did not work as expected.
    """
    def __init__(self, msg=None):
        Exception.__init__(self, msg)
        self.msg = msg
