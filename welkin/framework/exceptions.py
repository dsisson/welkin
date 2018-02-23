"""
    Custom Welkin exceptions, managed in one place.
"""


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


class PageIdentityException(Exception):
    """
        Raise this exception when a page fails its self validation of identity.
    """
    pass


class GoogleResultsCountException(Exception):
    """
        What we thought was a resulst count apparently was NOT.
    """
    pass
