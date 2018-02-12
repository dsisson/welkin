#!/usr/bin/python

import sys
import os
import time
import pytest

from welkin.framework import utils
from welkin.tests import configs

# get the timestamp for this test run
timestamp = time.strftime('%y%m%d-%H%M%S')
output_path = utils.generate_output_path(timestamp)  # used by conftest.py
folder = utils.create_output_folder(output_path)     # used by conftest.py


def main():
    """
    Setup the py.test call from the command line. This supports the combined use of markers and options,
    for example:
        python runner.py -k get_

    :return: None
    """
    # get the command line arguments and insert the timestamp for the reports output
    args = sys.argv[1:]
    args.append('-vv')
    args.append('--timestamp=%s' % timestamp)
    args.append('--output_target=%s' % folder)

    # don't generate the results report if this is a collect-only action
    if not '--collect-only' in args:
        args.append('--html=%s/results.html' % folder)

    plgns = [configs]
    print(plgns)
    print(args)

    # invoke pytest and pass in the command line arguments
    pytest.main(args, plugins=plgns)


if __name__ == "__main__":
    main()