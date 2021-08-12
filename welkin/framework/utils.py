import logging
import os
import json
import pprint

logger = logging.getLogger(__name__)


def generate_output_path(folder_name):
    """
        Take the supplied folder_name and generate the path to that folder (for output files).

        :param folder_name: str, name of target folder
    """
    # get the absolute path to the current directory
    raw_path_to_here = os.path.abspath(os.curdir)

    # convert it to a list
    path_elements = raw_path_to_here.split('/')

    # find the index for 'welkin'
    index = path_elements.index('welkin')

    # chop off everything from the first 'welkin' rightward
    first_part = path_elements[:index]

    # expect the output file to be in welkin/welkin/output
    first_part.extend(['welkin', 'output', folder_name])

    # convert the list back into a string
    path_to_output = '/'.join(first_part)
    logger.info('Generated output path "%s".' % path_to_output)

    return path_to_output


def create_output_folder(path_to_output):
    """
        Take the supplied path and create a folder for that path.

        :param path_to_output: str, name of target folder
    """
    if not os.path.isdir(path_to_output):
        os.makedirs(path_to_output)
        logger.info('created output folder at "%s".' % path_to_output)
    else:
        logger.info('output folder "%s" already exists.' % path_to_output)

    return path_to_output


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
                logger.warn(msg)
                pass

        formatted_content = content

    return formatted_content