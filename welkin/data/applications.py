import pytest
import logging

logger = logging.getLogger(__name__)

"""
    Maps that app name and tier to the hostname string. 
    
    This is a contrived example because Welkin isn't testing 
    any apps with multiple tiers. 
"""
app_tier_map = {
    'duckduckgo': {
        'int': {'domain': 'duckduckgo.com'},
        'stage': {'domain': 'duckduckgo.com'},
        'prod': {'domain': 'duckduckgo.com'}
    }
}


def get_app_url_for_tier(app, tier):
    """
        Extract the hostname for the appropriate `app` and `tier`
        values.

        :param app: str, the internal application name
        :param tier: str enum, a valid tier name
        :return hostname: str, hostname
    """
    hostname = app_tier_map[app][tier]
    logger.info(f"\nfound hostname '{hostname}' for app '{app}' on tier '{tier}'")
    return hostname
