import logging
import boto3

from welkin.framework import utils

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
            logger.info(f"\nAWS session created for '{self.region}': {self.session} ({id(self.session)})")


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
        # extract the boto3 object from the Welkin object
        self.session = session.session
        self.region = session.region

        self.resource_name = resource_name
        client = self.session.client(resource_name)
        self.client = client

    def get_password(self, aws_key_name, decrypt=False):
        """
            Get the value for key `aws_key_name` from the AWS
            Parameter store.

            This is really for any parameter in the AWS Parameter Store,
            but for disambiguation we call this a password operation.

            See the README for more context as well as AWS set up
            information to support passwords (parameters).

            :param aws_key_name: str, key name (looks likes a path)
            :param decrypt: bool, True or False; defaults to False
            :return password: str, value for aws_key_name
        """
        res = self.client.get_parameter(Name=aws_key_name,
                                        WithDecryption=decrypt)
        return res
