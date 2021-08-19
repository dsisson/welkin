import logging
import pytest
import time
import pprint
import os
import re
import json
import hashlib
from io import BytesIO

from welkin.framework import utils

logger = logging.getLogger(__name__)


def write_cookies_to_file(cookies, url, fname=''):
    """
        Save cookies as json to a file.

        :param cookies: list of dicts
        :param url: str, url for the current page
        :param fname: str, first part of filename, will be appended with
                           timestamp; defaults to empty string
        :return: None
    """
    filename = f"/{time.strftime('%H%M%S')}_{utils.path_proof_name(fname)}.txt"
    path = pytest.welkin_namespace['testrun_cookies_output'] + filename
    with open(path, 'w') as f:
        f.write(f"{url}\n")  # write the url as the first line
        f.write(utils.plog(cookies))
    logger.info(f"\nSaved cookies: {path}.")


def write_traffic_log_to_file(log, url, fname=''):
    """
        Save the browser network traffic log as json to a file.

        :param log:
        :param url: str, url for the current page
        :param fname: str, first part of filename, will be appended with
                           timestamp; defaults to empty string
        :return: None
    """
    # note: json files don't allow comments, so we'd not be able
    # to write the url to the file
    filename = f"/{time.strftime('%H%M%S')}_{utils.path_proof_name(fname)}.json"
    path = pytest.welkin_namespace['testrun_traffic_log_folder'] + filename

    wrapper = {}
    wrapper['_page'] = url
    wrapper['chrome network logs'] = log
    with open(path, 'a') as f:
        f.write(utils.plog(wrapper))
    logger.info(f"\nSaved traffic log: {path}.")


def write_console_log_to_file(log, url, fname=''):
    """
        Write the chrome devtools console logs to a file.

        :param log: dict
        :param url: str, url for the current page
        :param fname: str, first part of filename, will be appended with
                           timestamp; defaults to empty string
        :return: None
    """
    filename = f"/{time.strftime('%H%M%S')}_{utils.path_proof_name(fname)}.json"
    path = pytest.welkin_namespace['testrun_console_log_folder'] + filename

    # add key/value for the page url
    log.update({'_page': url})

    with open(path, 'a') as f:
        f.write(utils.plog(log))
    logger.info(f"\nSaved console logs (and bad headers): {path}.")
