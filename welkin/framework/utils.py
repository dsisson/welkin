import logging
import os
import json

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

        :param content: json content
        :return:

        The typical usage will look like this:
        >>> from welkin.framework import utils
        >>> my_json = res.json()
        >>> logger.info(utils.plog.my_json)
    """
    formatted_content = None
    try:
        formatted_content = json.dumps(content, indent=4, sort_keys=True)
    except (ValueError, TypeError):
        # oops, this wasn't actually json
        formatted_content = content
    return formatted_content