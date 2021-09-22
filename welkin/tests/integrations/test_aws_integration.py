import pytest
import logging

from welkin.framework import utils
from welkin.integrations.aws.aws import AWSSession, AWSClient

logger = logging.getLogger(__name__)


class AwsIntegrationTests(object):

    def test_integration_session(self):
        """
            Validation for the AWS integration code.
        """
        aws_region = 'us-west-1'

        # create a session object tied to the local default config
        # for region and IAM user
        session = AWSSession(region=aws_region)

        # create a client tied to this session
        client = AWSClient(session, resource_name='ssm')

        param_key = '/example/staging/my-app/password'
        expected_param_value = 'This is an example "password".'

        # get the value for the
        res = client.get_password(aws_key_name=param_key, decrypt=False)
        logger.info(f"\nAWS response:\n{utils.plog(res)}")

        assert res['Parameter']['Value'] == expected_param_value

    def test_integration_session_defaults(self, duckduckgo):
        """
            Validation for the AWS integration code with default args.
        """
        # create a session object tied to the local default config
        # for region and IAM user
        session = AWSSession()

        # create a client tied to this session
        client = AWSClient(session, resource_name='ssm')

        param_key = '/example/staging/my-app/password'
        expected_param_value = 'This is an example "password".'

        # get the value for the
        res = client.get_password(aws_key_name=param_key)
        logger.info(f"\nAWS response:\n{utils.plog(res)}")

        assert res['Parameter']['Value'] == expected_param_value

    def test_integration_session_fixture(self, auth):
        """
            Validation for the AWS integration code called as a fixture.

            run this with test_integration_session_fixture2 to
            check whether the session is getting created multiple
            times
        """
        session = auth

        # create a client tied to this session
        client = AWSClient(session, resource_name='ssm')

        param_key = '/example/staging/my-app/password'
        expected_param_value = 'This is an example "password".'

        # get the value for the
        res = client.get_password(aws_key_name=param_key, decrypt=False)
        logger.info(f"\nAWS response:\n{utils.plog(res)}")

        assert res['Parameter']['Value'] == expected_param_value

    def test_integration_session_fixture2(self, auth):
        """
            Validation for the AWS integration code called as a fixture.

            run this with test_integration_session_fixture to
            check whether the session is getting created multiple
            times
        """
        session = auth

        # create a client tied to this session
        client = AWSClient(session, resource_name='ssm')

        param_key = '/example/staging/my-app/password'
        expected_param_value = 'This is an example "password".'

        # get the value for the
        res = client.get_password(aws_key_name=param_key, decrypt=False)
        logger.info(f"\nAWS response:\n{utils.plog(res)}")

        assert res['Parameter']['Value'] == expected_param_value
