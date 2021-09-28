import logging

from welkin.framework import utils
from welkin.framework.exceptions import UserDataAccessException

logger = logging.getLogger(__name__)

"""
This user map is structured like this:
<<tier>>
    |- <<appname>>
        |- <<framework user id, aka "fuid">>
            |- details for this user 

This "path" is used to name and access the user passwords 
in the AWS ParameterStore. See integrations/aws/README_aws.md.
"""
app_user_map = {
    'int': {
        'duckduckgo': {
            'user01': {
                'app': 'duckduckgo',
                'email': 'int_user@example.com',
                'fuid': 'user01'
            }
        }
    },
    'stage': {
        'duckduckgo': {
            'user01': {
                'app': 'duckduckgo',
                'email': 'test_user@example.com',
                'fuid': 'user01'
            }
        }
    },
    'prod': {
        'duckduckgo': {
            'user01': {
                'app': 'duckduckgo',
                'email': 'prod_user@example.com',
                'fuid': 'user01'
            }
        }
    }
}


def get_specific_user(tier, app, fuid, verbose=False):
    """
        Return a single user `fuid` for tier + app.

        :param tier: str, one of 'int', 'stage', 'prod'
        :param app: str, the internal application name
        :param fuid: str, unique identifier for user of tier/app
        :param verbose: bool, whether to log additional information
        :return this_user: dict, data for this fuid
    """
    this_app = None

    # attempt to lookup the app first
    try:
        this_app = app_user_map[tier][app]
    except KeyError:
        msg = f"Unable to find app '{app}' in the '{tier}' tier data."
        logger.error(msg)
        raise UserDataAccessException(msg)

    # now look up the specific user id
    try:
        this_user = this_app[fuid]
        if verbose:
            logger.info(f"\nthis_user '{fuid}':\n{utils.plog(this_user)}")
        return this_user
    except KeyError:
        other_users = [u for u in this_app]
        msg = f"Unable to find user '{fuid}' in the '{tier}'/'{app}' " \
              f"data: {other_users}"
        logger.error(msg)
        raise UserDataAccessException(msg)
