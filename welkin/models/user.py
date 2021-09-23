import logging

from welkin.integrations.aws.aws import AWSClient
from welkin.framework import utils
from welkin.data.users import get_specific_user

logger = logging.getLogger(__name__)


class ApplicationUser():
    """
        This is the model for the user accounts of applications under test,
        and it allows for the abstraction of user data from the
        test code.

        example use from a test:
            >>> user = ApplicationUser(tier, appname, user_id)
            >>> user.fuid
            'user01'
    """
    def __init__(self, tier, appid, fuid, verbose=False):
        """
            Instantiate an object for this particular application user.

            :param tier: str enum, one of 'int', 'staging', 'prod'
            :param appid: str enum, key from data/applications.py
            :param fuid: str, ID for user
            :param verbose: bool, True to output additional information
        """
        self.tier = tier
        self.application = appid
        self.fuid = fuid
        self._populate_properties_from_user_data(verbose=True)
        self.password_key = self._generate_parameter_key()

    def _populate_properties_from_user_data(self, verbose=False):
        """
            Pull in the user account properties specified in data/uers.py
            and add them to the class instance.

            example data:
                'int': {
                    'duckduckgo': {
                        'user01': {
                            'app': 'duckduckgo',
                            'email': 'int_user@example.com',
                            'fuid': 'user01'
                        }
                    }
                },

            print(user):
                ApplicationUser({
                    'tier': 'stage',
                    'application': 'duckduckgo',
                    'fuid': 'user01',
                    'properties': {
                            'app': 'duckduckgo',
                            'email': 'test_user@example.com',
                            'fuid': 'user01'
                    },
                    'password_key': '/welkin/stage/duckduckgo/user01'
                })

            :param verbose: bool, True to output additional information
            :return: None
        """
        raw_props = get_specific_user(self.tier, self.application, self.fuid)
        self.properties = {}
        for key in raw_props:
            self.properties[key] = raw_props[key]
        logger.info(f"\npopulated properties:\n{utils.plog(self.properties)}")

    def _generate_parameter_key(self):
        """
            Assemble the steps in the user data path
            (from data/users.py) into the parameter_key used in the
            AWS Parameter Store ARNs.

            :return param_key: str, key name (looks likes a path)
        """
        param_key = f"/welkin/{self.tier}/{self.application}/{self.fuid}"
        return param_key

    def get_password_from_aws(self, aws_session, verbose=False):
        """
            Make an AWS call to retrieve the password for this user.

            :param aws_session: AWS session object
            :param verbose: bool, True to output additional information
            :return: None
        """
        resource = 'ssm'  # AWS System manager is used for parameters
        client = AWSClient(aws_session, resource_name=resource)

        # make the AWS get parameter call
        res = client.get_password(aws_key_name=self.password_key,
                                  decrypt=False)
        if verbose:
            msg1 = f"AWS response:\n{utils.plog(res)}"
            msg2 = f"\n\n\n{'#-' * 50}\nNOTE: Don't log passwords!" \
                   f"\n{msg1}\n{'#-' * 50}\n\n\n"
            logger.info(msg2)
        self.password = res['Parameter']['Value']

    def __str__(self):
        """
           Provide a good-looking representation for the
           ApplicationUser object.

           Note: NEVER DISPLAY THE PASSWORD VALUE!

           If the `password` property has been set, create a new non-copied
           dict of properties with the password value removed.

           :return: str of properties
        """
        properties = self.__dict__
        keys = properties.keys()
        if not 'password' in keys:
            return f"ApplicationUser({properties})"
        else:
            cleaned_keys = [k for k in keys if not k == 'password']
            cleaned_props = {k:properties[k] for k in cleaned_keys}
            cleaned_props['password'] = 'value redacted'
            return f"ApplicationUser({cleaned_props})"
