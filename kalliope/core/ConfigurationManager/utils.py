import inspect
import os


def get_root_kalliope_path():
    # here we are in /an/unknown/path/kalliope/core/ConfigurationManager
    current_script_path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    # get parent dir. Now we are in /an/unknown/path/kalliope
    kalliope_root_path = os.path.normpath(current_script_path + os.sep + os.pardir + os.sep + os.pardir)
    return kalliope_root_path