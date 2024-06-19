import logging
import pytest
import time
import json

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
    filename = f"{time.strftime('%H%M%S')}_{utils.path_proof_name(fname)}.txt"
    path = pytest.custom_namespace['current test case']['cookies folder'] / filename
    with open(path, 'w') as f:
        f.write(f"{url}\n")  # write the url as the first line
        f.write(utils.plog(cookies))
    logger.info(f"\nSaved cookies: {path}.")


def write_network_log_to_file(log, url, fname=''):
    """
        Save the browser network log as json to a file.

        :param log:
        :param url: str, url for the current page
        :param fname: str, first part of filename, will be appended with
                           timestamp; defaults to empty string
        :return: None
    """
    # note: json files don't allow comments, so we'd not be able
    # to write the url to the file
    filename = f"{time.strftime('%H%M%S')}_{utils.path_proof_name(fname)}.json"
    path = pytest.custom_namespace['current test case']['network folder'] / filename

    wrapper = {}
    wrapper['_page'] = url
    wrapper['chrome network logs'] = log
    with open(path, 'a') as f:
        f.write(utils.plog(wrapper))
    logger.info(f"\nSaved browser network log: {path}.")


def write_metrics_log_to_file(log, url, fname=''):
    """
        Save the browser metrics log as json to a file.

        :param log: dict, browser metrics log
        :param url: str, url for the current page
        :param fname: str, first part of filename, will be appended with
                           timestamp; defaults to empty string
        :return:
    """
    # note: json files don't allow comments, so we'd not be able
    # to write the url to the file. Instead, insert a kv pair into dict
    filename = f"{time.strftime('%H%M%S')}_{utils.path_proof_name(fname)}.json"
    path = pytest.custom_namespace['current test case']['metrics folder'] / filename

    wrapper = {}
    wrapper['_page'] = url
    wrapper.update(log)
    with open(path, 'a') as f:
        f.write(utils.plog(wrapper))
    logger.info(f"\nSaved browser metrics log: {path}.")


def write_console_log_to_file(log, url, fname=''):
    """
        Write the chrome devtools console logs to a file.

        :param log: dict
        :param url: str, url for the current page
        :param fname: str, first part of filename, will be appended with
                           timestamp; defaults to empty string
        :return: None
    """
    filename = f"{time.strftime('%H%M%S')}_{utils.path_proof_name(fname)}.json"
    path = pytest.custom_namespace['current test case']['console folder'] / filename

    # add key/value for the page url
    log.update({'_page': url})

    with open(path, 'a') as f:
        f.write(utils.plog(log))
    logger.info(f"\nSaved console logs (and bad headers): {path}.")


def write_webstorage_to_files(data, current_url, pageobject_name,
                              event):
    """
        Write the localStorage and sessionStorage content to a log file.

        Note 1: the data is a cleaned up representation of the json data;
                however, the file is NOT json.
        Note 2: the timing of when the content is written may be significant.

        :param data: list, localStorage dict and sessionStorage dict
        :param current_url: str, url for the current page
        :param pageobject_name: str, name for the current pageobject
        :param event: str, descriptor for an interaction with the React app
        :return: None
    """
    base_filename = f"{time.strftime('%H%M%S')}_" \
                    f"{utils.path_proof_name(event)}"
    path = pytest.custom_namespace['current test case']['webstorage folder'] / base_filename

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

        Note: several welkin key-value pairs will be inserted into that data.

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

        Note: several welkin key-value pairs will be inserted into that data.

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


def write_request_to_file(response, url, fname=''):
    """
        Save the request and response headers and payload.

        Note that the request info is extracted from the response content.

        :param response: requests Response object
        :param url: str, url for the current page
        :param fname: str, first part of filename, will be appended with
                           timestamp; defaults to empty string
        :return: None
    """
    filename = f"{time.strftime('%H%M%S')}_{utils.path_proof_name(fname)}.txt"
    path = pytest.custom_namespace['current test case']['requests folder'] / filename
    boundary = None
    with open(path, 'a') as f:
        f.write(f"{url}\n\n")  # write the url as the first line
        f.write("###### REQUEST ####### \n")
        f.write("HEADERS\n")
        try:
            # the request header MUST have the Content-Type key-value pair
            # if not, raise an exception and kill the test
            content_type = response.request.headers['Content-Type']
        except KeyError:
            msg = f"Missing header content-type field in request to {url}"
            logger.error(msg)
            raise ValueError(msg)
        if 'boundary' in content_type:
            # this is a POST, it must have the multi-part content-type, so
            # extract the boundary str used between binary attachments
            boundary = content_type[content_type.index('boundary=') + 9:]
        f.write(utils.plog(response.request.headers))

        if response.request.body:
            # it will be as BODY (None) in file because content_type is not found in headers
            f.write(f"\n\nBODY ({content_type})\n")
            if isinstance(response.request.body, bytes):
                # this was a binary upload, so decode it as a
                # unicode str in order to write it to the file
                logger.warning("response.request.body cast as string.")
                f.write("--decoded from bytes--\n")
                if boundary:
                    # this is a multi-part form body
                    # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Disposition
                    body = response.request.body.decode('utf-8', 'backslashreplace')
                    cleaned_body = body.replace('\r\n\r\n\n\r\n', '\n\n')
                    f.write(cleaned_body)
                else:
                    f.write("don't know what happened with this request body;\n"
                            "probably a POST with bytes.")

            else:
                try:
                    f.write(utils.plog(json.loads(response.request.body)))
                except UnicodeDecodeError:
                    logger.warning("got UnicodeDecodeError.")
                    f.write("-- byte string snipped --")
                except json.decoder.JSONDecodeError:
                    logger.warning("got json.decoder.JSONDecodeError.")
                    f.write(utils.plog(response.request.body))

        f.write("\n\n###### RESPONSE ####### \n")
        f.write("HEADERS\n")
        f.write(utils.plog(response.headers))
        f.write("\n\nRESPONSE STATUS CODE\n")
        f.write(f"response server status: {response.status_code}")
        f.write("\n\nPAYLOAD\n")
        try:
            f.write(utils.plog(response.json()))
        except json.decoder.JSONDecodeError:
            # this could be an xml byte response
            f.write(utils.plog(response.content))

        f.write(f"\n\n{'~' * 45}\n\n")

    logger.info(f"Saved headers: {path}")


def write_sdk_response_to_file(response, sdk_app, fname=''):
    """
        Save the response from an SDK. Unlike typical API calls, the
        SDK calls don't necessarily have the standard http request data
        patterns.

        These SDKs will be wrappers in the welkin/integrations folder.

        :param response: SDK response, probably json or a dict
        :param sdk_app: str name of the SDK
        :param fname: str, first part of filename, will be appended with
                           timestamp; defaults to empty string
        :return: None
    """
    filename = f"{time.strftime('%H%M%S')}_{utils.path_proof_name(fname)}.json"
    path = pytest.custom_namespace['current test case']['integrations folder'] / filename
    with open(path, 'a') as f:
        f.write(utils.plog(response))


def write_axe_log_to_file(axe_results, fname):
    """
        Save the axe accessibility audit results to a json file.

        :param axe_results: dict, axe accessibility audit results
        :param fname: str, first part of filename
        :return: None
    """
    filename = f"{time.strftime('%H%M%S')}_{utils.path_proof_name(fname)}.json"
    path = pytest.custom_namespace['current test case']['accessibility folder'] / filename
    logger.info(f"\nWriting accessibility logs to {filename}")
    with open(path, 'a') as f:
        f.write(utils.plog(axe_results))
