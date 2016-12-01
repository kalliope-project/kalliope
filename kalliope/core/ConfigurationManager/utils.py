import inspect
import logging
import os

logging.basicConfig()
logger = logging.getLogger("kalliope")


def get_root_kalliope_path():
    # here we are in /an/unknown/path/kalliope/core/ConfigurationManager
    current_script_path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    # get parent dir. Now we are in /an/unknown/path/kalliope
    kalliope_root_path = os.path.normpath(current_script_path + os.sep + os.pardir + os.sep + os.pardir)
    return kalliope_root_path


def get_real_file_path(file_path_to_test):
    """
    Try to return a full path from a given <file_path_to_test>
    If the path is an absolute on, we return it directly.

    If the path is relative, we try to get the full path in this order:
    - from the current directory where kalliope has been called + the file_path_to_test.
    Eg: /home/me/Documents/kalliope_config
    - from /etc/kalliope + file_path_to_test
    - from the default file passed as <file_name> at the root of the project

    :param file_path_to_test file path to test
    :type file_path_to_test: str
    :return: absolute path to the file file_path_to_test
    """

    if not os.path.isabs(file_path_to_test):
        path_order = {
            1: os.getcwd() + os.sep + file_path_to_test,
            2: "/etc/kalliope" + os.sep + file_path_to_test,
            3: get_root_kalliope_path() + os.sep + file_path_to_test
        }

        for key in sorted(path_order):
            new_file_path_to_test = path_order[key]
            logger.debug("Try to load file from %s: %s" % (key, new_file_path_to_test))
            if os.path.isfile(new_file_path_to_test):
                logger.debug("File found in %s" % new_file_path_to_test)
                return new_file_path_to_test

    return file_path_to_test
