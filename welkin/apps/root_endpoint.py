import logging
import requests
import json
import uuid
from cerberus import Validator

from welkin.framework import utils
from welkin.framework import utils_file
from welkin.framework.exceptions import JsonPayloadException

logger = logging.getLogger(__name__)


class RootEndpoint(object):
    template_load = 'Instantiated endpoint object "%s".'

    #  create a request session object to be reused for subsequent API calls
    session = requests.Session()

    def generate_uuid(self):
        """
            Generate a v4 UUID, which is random.

            Most APIs require a Universally Unique IDentifier;
            see https://datatracker.ietf.org/doc/html/rfc4122.html

            :return: str UUID
        """
        return str(uuid.uuid4())

    def set_headers(self):
        """
            Create the core set of headers to be used on all API requests.

            :return: None
        """
        self.headers = {
            'Content-Type': 'application/json',
            'X-RequestID': self.generate_uuid(),
        }

    def get(self, url, expect_status=200, expect_errors=False, use_session=True,
            params=None, verbose=False, **kwargs):
        """
            Perform an HTTP GET action, and return the request response object.

            This wraps the requests module's GET call.

            Optionally specify an expected status code; use this to functionally
            test an endpoint.

            Unhappy path testing:
                1. set the `expect_status` argument to the HTTP status code you
                expect with this request. If you are negative testing, you will
                create a request that you expect to fail with a specific status
                code, and you will set this argument accordingly. The test should
                PASS if it returns the correct error behavior.
                2. If you create a request that should return errors, set the
                `expect_errors` argument to True. This triggers code flows to
                evaluate an error response as an expected response.

            :param url: str url for the HTTP request
            :param expect_status: int, the expected valid HTTP status code
            :param expect_errors: bool, True if we expect application errors
            :paeam use_session: bool, whether to use the requests session object
                                defaults to True
            :param kwargs: dict, keys & values to get dumped to json
            :return res: requests Response object
        """
        # make the request
        logger.info(f"Getting url: {url}")
        logger.info(f"\nHeaders: {utils.plog(self.headers)}")
        if verbose:
            logger.info(f"\nparams: {utils.plog(params)}")
        if params:
            if use_session:
                res = self.session.get(
                    url,
                    headers=self.headers,
                    verify=True,
                    params=params
                )
            else:
                logger.warning("Choosing not to use the requests session object.")
                res = requests.get(
                    url,
                    headers=self.headers,
                    verify=True,
                    params=params
                )
        else:
            if use_session:
                res = self.session.get(
                    url,
                    headers=self.headers,
                    verify=True)
            else:
                logger.warning("Choosing not to use the requests session object.")
                res = requests.get(
                    url,
                    headers=self.headers,
                    verify=True)

        if params:
            final_url = res.url
        else:
            final_url = url

        logger.info(f"\nResponse code: {res.status_code}")
        logger.info(f"\nResponse json:\n{utils.plog(res.json())}")

        # write the response headers to a file
        utils_file.write_request_to_file(res, final_url, fname=self.name)

        # check for good, bad, and error results
        # parsed_results = self._parse_response(res, expect_status, expect_errors, **kwargs)
        return res

    def post(self, url, expect_status=200, expect_errors=False, use_session=True,
             params=None, verbose=False, **kwargs):
        """
            Perform an HTTP POST action, and return the request response object.

            This wraps the requests module's POST call.

            Optionally specify an expected status code; use this to functionally
            test an endpoint.

            Unhappy path testing:
                1. set the `expect_status` argument to the HTTP status code you
                expect with this request. If you are negative testing, you will
                create a request that you expect to fail with a specific status
                code, and you will set this argument accordingly. The test should
                PASS if it returns the correct error behavior.
                2. If you create a request that should return errors, set the
                `expect_errors` argument to True. This triggers code flows to
                evaluate an error response as an expected response.

            :param url: str url for the HTTP request
            :param expect_status: int, the expected valid HTTP status code
            :param expect_errors: bool, True if we expect application errors
            :param kwargs: dict, keys & values to get dumped to json
            :return res: requests Response object
        """
        # make the request
        logger.info(f"Posting url: {url}")
        logger.info(f"\nHeaders: {utils.plog(self.headers)}")
        if verbose:
            logger.info(f"\nparams: {utils.plog(params)}")
        if params:
            if use_session:
                res = self.session.post(
                    url,
                    headers=self.headers,
                    data=json.dumps(kwargs),
                    verify=True,
                    params=params
                )
            else:
                logger.warning("\nChoosing not to use the requests session object.")
                res = requests.post(
                    url,
                    headers=self.headers,
                    data=json.dumps(kwargs),
                    verify=True,
                    params=params
                )
        else:
            if use_session:
                res = self.session.post(
                    url,
                    headers=self.headers,
                    data=json.dumps(kwargs),
                    verify=True)
            else:
                logger.warning("\nChoosing not to use the requests session object.")
                res = requests.post(
                    url,
                    headers=self.headers,
                    data=json.dumps(kwargs),
                    verify=True)

        if params:
            final_url = res.url
        else:
            final_url = url

        logger.info(f"\nResponse code: {res.status_code}")
        logger.info(f"\nResponse json:\n{utils.plog(res.json())}")

        # write the response headers to a file
        utils_file.write_request_to_file(res, final_url, fname=self.name)

        # check for good, bad, and error results
        # parsed_results = self._parse_response(res, expect_status, expect_errors, **kwargs)
        return res

    def verify_keys_in_response(self, response_keys, verbose=False):
        """
            Verify that the endpoint response contains the expected top-level
            keys.

            NOTE: this is deprecated in favor of validate_schema()

            :param response_keys: dict_keys, the top-level response keys
            :param verbose: bool, determines whether to output additional logging
            :return: True if keys are equal, else raise exception
        """
        # be strict about checking keys
        expected = self.expected_keys
        actual = list(response_keys)
        actual.sort()
        if verbose:
            logger.info(f"\nComparing expected keys '{expected}'"
                        f"\nto"
                        f"\nactual keys '{actual}'.")

        if sorted(expected) == sorted(actual):
            logger.info('Comparison results: Keys are equal.')
            return True
        else:
            logger.error('Comparison results: Keys are NOT equal.')
            logger.error(f"Expected keys:\n{utils.plog(expected)}")
            logger.error(f"Actual keys:\n{utils.plog(actual)}")
            raise JsonPayloadException("Actual keys don't match expected keys.")

    def validate_schema(self, response_data, verbose=False):
        """
            Verify that the endpoint response contains the expected top-level
            keys, and that the value data types match the expected types
            as defined by the PO's schema property.

            Example schema:
                schema = {
                    'current_page': {'type': 'integer'},
                    'limit': {'type': 'integer'},
                    'results': {'type': 'list'},
                    'search_term': {'type': 'string'},
                    'status': {'type': 'integer'},
                }

            If the schema does NOT validate, raise a JsonPayloadException.
            If you are unhappy path testing, handle that in the calling test.

            :param response_data: dict, response data from API call
            :param verbose: bool, determines whether to output additional logging
            :return result: bool, True if schema validated
        """
        if verbose:
            logger.info(f"\nschema for '{self.name}':"
                        f"\n{utils.plog(self.schema)}")
        # instantiate the validator
        validator = Validator()
        result = validator.validate(response_data, self.schema)
        logger.info(f"\nvalidation result: {result}")
        if not result:
            errors = validator.errors
            msg = f"Response data for '{self.name}' API call failed schema " \
                  f"validation: {errors}"
            logger.error(msg)
            raise JsonPayloadException(msg)
        else:
            return result
