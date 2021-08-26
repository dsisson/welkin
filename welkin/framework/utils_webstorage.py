from copy import deepcopy
import deepdiff
import dpath.util
import json
import logging

from welkin.framework import utils

logger = logging.getLogger(__name__)


def convert_web_storage_data_to_dict(content, stype, verbose=False):
    """
        Window sessionStorage consists of string keys and string values.

        Convert this into an easier-to-parse data structure that we
        can traverse.

        Keys are single quoted, and are kept as-is. Values, however,
        need to be cleaned up. Loop over values and loads as json; if the
        result is a dict, json-load *that* too.

        :param content: dict, returned from window.sessionContent
        :param stype: str enum, 'local' or 'session'
        :param verbose: bool, whether to output additional logging
        :return new_content: dict, cleaned up data structure
    """
    # container for "cleaned" keys and values
    new_content = {}

    # use a deepcopy to avoid side effects
    old_content = deepcopy(content)

    def _to_json(data):
        try:
            jdata = json.loads(data)
            return jdata
        except TypeError:
            # if it's not a string, that's ok; return the original value
            return data
        except json.decoder.JSONDecodeError:
            # if it's a string but not a dict, that's ok; return original value
            return data

    # iterate over the top-level keys
    for k1, v1 in old_content.items():
        if verbose:
            logger.info(f"--->> {k1}, {v1}")
        first_data = _to_json(v1)
        new_content[k1] = first_data
        if isinstance(first_data, dict):
            # iterate over the 2nd-tier keys
            for k2, v2 in first_data.items():
                if verbose:
                    logger.info(f"--->> {k2}, {v2}")
                second_data = _to_json(v2)
                new_content[k1][k2] = second_data

    if verbose:
        logger.info(f"{stype}Storage data converted to dict.")
    return new_content
