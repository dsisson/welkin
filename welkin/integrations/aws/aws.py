import logging
import boto3

from welkin.framework import utils
from welkin.framework import utils_file

logger = logging.getLogger(__name__)


class AWSSession:

    def __init__(self, region='us-west-1', verbose=False):
        """
            Create an instance of an AWS session, which is tied to an IAM
            identity and a region. A session can support multiple clients for
            different services.

            Example usage:
                >>> session = AWSSession()

            :param region: str, AWS region identifier
            :param verbose: bool, True to output additional information
        """
        self.session = boto3.Session(region_name=region)
        self.region = region
        if verbose:
            logger.info(f"\nAWS session created for '{self.region}': "
                        f"{self.session} ({id(self.session)})")


class AWSClient:

    def __init__(self, session, resource_name):
        """
            Create a client for service `resource_name` using
            session `session`.

            Example usage:
                >>> session = AWSSession()
                >>> client = AWSClient(session, resource_name='ssm')

            :param session: boto3 session object
            :param resource_name: str, service/resource identifier
        """
        self.name = 'AWS client'
        # extract the boto3 object from the Welkin object
        self.session = session.session
        self.region = session.region

        self.resource_name = resource_name
        client = self.session.client(resource_name)
        self.client = client

    def get_parameter_data(self, aws_key_name, decrypt=False):
        """
            Get the value (and all the associated meta data) for key
            `aws_key_name` from the AWS Parameter store.

            If this used for a password, set the parameter value in AWS
            as a Secure String. This will encrypt the value using the
            AWS KMS service, so if you are getting a encrypted password,
            pass the `decrypt=True` argument.

            See the README for more context as well as AWS set up
            information to support passwords as parameters.

            :param aws_key_name: str, key name (looks likes a path)
            :param decrypt: bool, True or False; defaults to False
            :return password: str, value for aws_key_name
        """
        res = self.client.get_parameter(Name=aws_key_name,
                                        WithDecryption=decrypt)
        # write the response headers to a file
        utils_file.write_sdk_response_to_file(
            utils.strip_password_for_reporting(res),
            sdk_app=self.name,
            fname='get param')
        return res
