import pytest
import logging

from welkin.framework import utils
from welkin.models.user import ApplicationUser
from welkin.integrations.aws.aws import AWSSession, AWSClient

TIER = pytest.custom_namespace.get('tier')
logger = logging.getLogger(__name__)


class AwsIntegrationTests(object):

    def test_integration_session(self):
        """
            Validation for the AWS integration code.
        """
        aws_region = 'us-west-1'
        tier = TIER
        appname = 'dummy_app'
        user = 'user01'
        param_key = f"/welkin/{tier}/{appname}/{user}"
        expected_param_value = f"secure password for user \"{param_key}\""

        # create a session object tied to the local default config
        # for region and IAM user
        session = AWSSession(region=aws_region)

        # create a client tied to this session
        client = AWSClient(session, resource_name='ssm')

        # make the AWS get parameter call
        res = client.get_parameter_data(aws_key_name=param_key, decrypt=True)
        logger.info(f"\nAWS response:\n"
                    f"{utils.plog(utils.strip_password_for_reporting(res))}")

        # check the expected parameter (aka the "password")
        actual_param_value = res['Parameter']['Value']
        assert actual_param_value == expected_param_value

    def test_integration_session_defaults(self, duckduckgo):
        """
            Validation for the AWS integration code with default args.
        """
        tier = TIER
        appname = 'dummy_app'
        user = 'user01'
        param_key = f"/welkin/{tier}/{appname}/{user}"
        expected_param_value = f"secure password for user \"{param_key}\""

        # create a session object tied to the local default config
        # for region and IAM user
        session = AWSSession()

        # create a client tied to this session
        client = AWSClient(session, resource_name='ssm')

        # make the AWS get parameter call
        res = client.get_parameter_data(aws_key_name=param_key, decrypt=True)
        logger.info(f"\nAWS response:\n"
                    f"{utils.plog(utils.strip_password_for_reporting(res))}")

        # check the expected parameter (aka the "password")
        actual_param_value = res['Parameter']['Value']
        assert actual_param_value == expected_param_value

    def test_integration_session_fixture(self, auth):
        """
            Validation for the AWS integration code called as a fixture.

            run this with test_integration_session_fixture2 to
            check whether the session is getting created multiple
            times
        """
        # setup
        tier = TIER
        appname = 'dummy_app'
        user = 'user01'
        param_key = f"/welkin/{tier}/{appname}/{user}"
        expected_param_value = f"secure password for user \"{param_key}\""
        session = auth

        # create a client tied to this session
        client = AWSClient(session, resource_name='ssm')

        # make the AWS get parameter call
        res = client.get_parameter_data(aws_key_name=param_key, decrypt=True)
        logger.info(f"\nAWS response:\n"
                    f"{utils.plog(utils.strip_password_for_reporting(res))}")

        # check the expected parameter (aka the "password")
        actual_param_value = res['Parameter']['Value']
        assert actual_param_value == expected_param_value

    def test_integration_session_fixture2(self, auth):
        """
            Validation for the AWS integration code called as a fixture.

            run this with test_integration_session_fixture to
            check whether the session is getting created multiple
            times
        """
        # setup
        tier = TIER
        appname = 'dummy_app'
        user = 'user01'
        param_key = f"/welkin/{tier}/{appname}/{user}"
        expected_param_value = f"secure password for user \"{param_key}\""
        session = auth

        # create a client tied to this session
        client = AWSClient(session, resource_name='ssm')

        # make the AWS get parameter call
        res = client.get_parameter_data(aws_key_name=param_key, decrypt=True)
        logger.info(f"\nAWS response:\n"
                    f"{utils.plog(utils.strip_password_for_reporting(res))}")

        # check the expected parameter (aka the "password")
        actual_param_value = res['Parameter']['Value']
        assert actual_param_value == expected_param_value

    def test_integration_session_fixture_user(self, auth):
        """
            Validation for the AWS integration code called as a fixture,
            and using the User model.
        """
        # setup
        tier = TIER
        appname = 'dummy_app'
        user_id = 'user01'
        param_key = f"/welkin/{tier}/{appname}/{user_id}"
        expected_param_value = f"secure password for user \"{param_key}\""
        session = auth

        # set up user object
        user = ApplicationUser(tier, appname, user_id)
        logger.info(f"\n~~~~> user object:\n{user}")

        # get the password
        user.get_password_from_aws(session, decrypt=True, verbose=True)
        logger.info(f"\n~~~~> user object:\n{user}")

        # check the expected parameter (aka the "password")
        # NOTE: CAREFUL WHEN ACCESSING OR COMPARING PASSWORDS
        actual_param_value = user.password
        assert actual_param_value == expected_param_value

    def test_integration_session_fixture_secure_user(self, auth):
        """
            Validation for the AWS integration code called as a fixture,
            and using the User model.
        """
        # setup
        tier = TIER
        appname = 'dummy_app'
        user_id = 'user01'
        # this param_key is just used here for logging and;
        # the key used in the AWS called is generated in the
        # user model
        param_key = f"/welkin/{tier}/{appname}/{user_id}"
        expected_param_value = f"secure password for user \"{param_key}\""
        session = auth

        # set up user object
        user = ApplicationUser(tier, appname, user_id)
        logger.info(f"\n~~~~> user object:\n{user}")

        # get the password
        user.get_password_from_aws(session, verbose=True, decrypt=True)
        logger.info(f"\n~~~~> user object:\n{user}")

        # check the expected parameter (aka the "password")
        # NOTE: CAREFUL WHEN ACCESSING OR COMPARING PASSWORDS
        actual_param_value = user.password
        assert actual_param_value == expected_param_value
