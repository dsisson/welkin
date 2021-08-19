import logging
import pytest
import time

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


def write_webstorage_to_files(data, current_url, pageobject_name,
                              filename, event=None):
    """
        Write the localStorage and sessionStorage content to a log file.

        Note 1: the data is a cleaned up representation of the json data;
                however, the file is NOT json.
        Note 2: the timing of when the content is written may be significant.

        :param data: list, localStorage dict and sessionStorage dict
        :param current_url: str, url for the current page
        :param pageobject_name: str, name for the current pageobject
        :param filename: str, custom filename, if provided
        :param event: str, descriptor for an interaction with the React app
        :return: None
    """
    if filename:
        # use the specified custom filename
        base_filename = f"{time.strftime('%H%M%S')}_{filename}"
    else:
        # generate a filename
        base_filename = f"/{time.strftime('%H%M%S')}_" \
                        f"{utils.path_proof_name(pageobject_name)}"
    path = pytest.welkin_namespace['testrun_webstorage_log_folder'] + base_filename

    # unpack the data
    local_storage, session_storage = data

    # write the local storage
    local_filename = f"{path}_local.json"
    _write_local_to_file(local_storage, event, pageobject_name,
                         current_url, local_filename)

    # write the session storage
    session_filename = f"{path}_session.json"
    _write_session_to_file(session_storage, event, pageobject_name,
                           current_url, session_filename)


def _write_local_to_file(data, event, pageobject_name, source_url, output_url):
    """
        Write the local storage to a json file in the webstorage folder.

        Note: several sweord key-value pairs will be inserted into that data.

        :param data: dict of local storage log pulled from the browser
        :param event: str, descriptor for an interaction with the React app
        :param pageobject_name: str, name of pageobject
        :param source_url: str, full url of the page that generated the logs
        :param output_url: str, full local path for the output file
        :return: None
    """
    # add key/value for the page url
    data.update({'_storage type': 'local'})
    data.update({'_page': source_url})
    data.update({'_page object name': pageobject_name})
    data.update({'_precipitating event': event})

    with open(output_url, 'a') as f:
        f.write(utils.plog(data))
    logger.info(f"Saved local storage log: {output_url}.")


def _write_session_to_file(data, event, pageobject_name, source_url, output_url):
    """
        Write the session storage to a json file in the webstorage folder.

        Note: several sweord key-value pairs will be inserted into that data.

        :param data: dict of session storage log pulled from the browser
        :param event: str, descriptor for an interaction with the React app
        :param pageobject_name: str, name of pageobject
        :param source_url: str, full url of the page that generated the logs
        :param output_url: str, full local path for the output file
        :return: None
    """
    # add key/value for the page url
    data.update({'_storage type': 'session'})
    data.update({'_page': source_url})
    data.update({'_page object name': pageobject_name})
    data.update({'_precipitating event': event})

    with open(output_url, 'a') as f:
        f.write(utils.plog(data))
    logger.info(f"Saved session storage log: {output_url}.")
