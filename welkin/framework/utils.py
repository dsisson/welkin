import logging
import os
import json
import time
import pathlib
import pprint
import pytest

logger = logging.getLogger(__name__)


def create_testrun_folder(timestamped_name):
    """
        Every pytest invocation triggers a bunch of logging actions. During
        the pytest start up routines, logging is enabled and configured,
        including the creation of timestamped folders for the output, which is
        managed below.

        :param timestamped_name:
        :return: tuple, welkin_root_path & testrun_path
    """
    # Get the absolute path to the current local directory.
    # This Path object will look like
    # PosixPath('/Users/<<name>>/devc/welkin/welkin')
    base_path = pathlib.Path.cwd()

    # Get the path parts up to and including the first instance of `welkin`.
    # We can't be certain that we are in the correct directory for running
    # welkin, so focus on the first "welkin" instance and build from there.
    parts = base_path.parts[:base_path.parts.index('welkin') + 1]

    # generate the path to the output folder
    welkin_root_path = pathlib.Path('/').joinpath(*list(parts)) / 'welkin'
    output_path = pathlib.Path('/').joinpath(*list(parts)) / 'welkin/output'
    testrun_path = output_path / timestamped_name

    # create the output path if it doesn't exist
    if not output_path.exists():
        output_path.mkdir()

    # create the testrun folder (it won't already exist)
    if not testrun_path.exists():
        testrun_path.mkdir()

    return welkin_root_path, testrun_path


def create_testrun_subfolder(path, folder):
    """
        Create a folder `folder` at path `path`.

        :param path:
        :param folder:
        :return:
    """
    # generate the path to the output subfolder
    folder_path = path / folder
    if not folder_path.exists():
        folder_path.mkdir()
    logger.info(f"Created sub-folder: {str(folder)}")
    return folder_path


def path_proof_name(name):
    """
        Some characters used in naming page objects or screenshots are
        not safe for paths, so clean up those names.

        :param name: str, name to be used for a file
        :return clean_name: transformed and presumed safe name
    """
    if not name:
        clean_name = 'None'
    else:
        # the most common problems are a slash
        clean_name = name.replace('/', '-')
        # and spaces
        clean_name = clean_name.replace(' ', '_')
        # and quotes
        clean_name = clean_name.replace('"', '')
        clean_name = clean_name.replace("'", '')

    return clean_name


def plog(content):
    """
        Format json content for pretty printing to the logger.

        If `content` is not json, try to identify what it is and then try
        to format it appropriately.

        :param content: assumed to be json
        :return formatted_content:

        The typical usage will look like this:
        >>> from welkin.framework import utils
        >>> my_json = res.json()
        >>> logger.info(utils.plog.my_json)
    """
    # set a default pass-through value of an empty string in order
    # to catch None, because if a calling method tries to write()
    # the output of plog() will error out in the attempt.
    formatted_content = ''
    try:
        formatted_content = json.dumps(content, indent=4, sort_keys=True)
    except (ValueError, TypeError):
        # oops, this wasn't actually json

        # try pretty-printing based on the guessed content type
        from requests.structures import CaseInsensitiveDict
        import deepdiff

        if isinstance(content, dict):
            formatted_content = pprint.pformat(content, indent=1, width=100)
        elif isinstance(content, list):
            formatted_content = pprint.pformat(content, indent=1, width=100)
        elif isinstance(content, CaseInsensitiveDict):
            formatted_content = pprint.pformat(dict(content), indent=1, width=100)
        elif isinstance(content, deepdiff.diff.DeepDiff):
            formatted_content = pprint.pformat(content, indent=1, width=160, depth=4)
        elif isinstance(content, bytes):
            # is this XML?
            if content[:5] == b'<?xml':
                import xml.dom.minidom
                xml = xml.dom.minidom.parseString(content)
                formatted_content = str(xml.toprettyxml())
            else:
                # no, this is some other kind of byte string
                msg = f"Unable to pretty print the content that starts with {content[:20]}"
                logger.warning(msg)
                pass

    return formatted_content
