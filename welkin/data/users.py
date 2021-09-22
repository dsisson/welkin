import logging
from welkin.framework import utils

logger = logging.getLogger(__name__)


app_user_map = {
    'int': {
        'duckduckgo': {
            'app': 'duckduckgo',
            'email': 'int_user@example.com'
        }
    },
    'stage': {
        'duckduckgo': {
            'app': 'duckduckgo',
            'email': 'test_user@example.com'
        }
    },
    'prod': {
        'duckduckgo': {
            'app': 'duckduckgo',
            'email': 'prod_user@example.com'
        }
    }
}


def get_users_for_tier(tier, app=None, verbose=False):
    """
     Extract the test users for the specified tier and specified app.

     :param tier: str, one of 'int', 'stage', 'prod'
     :param app: str, defaults to None
     :param verbose: bool, whether to log additional information
     :return: dict of users
     """
    logger.info(f"Getting tier '{tier}' users for '{app if app else 'all apps'}'")
    these_users = app_user_map[tier][app]
    if verbose:
        logger.info('\nFound users:\n%s' % utils.plog(these_users))
    return these_users
