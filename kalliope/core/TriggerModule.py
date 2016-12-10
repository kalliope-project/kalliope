import logging

from kalliope.core.Utils import Utils

logging.basicConfig()
logger = logging.getLogger("kalliope")


class TriggerModule(object):
    """
    Mother class of a trigger object
    """

    def __init__(self):
        super(TriggerModule, self).__init__()

    @staticmethod
    def get_file_from_path(file_path):
        """
        Trigger can be based on a model file, or other file.
        If a file is precised in settings, the path can be relative or absolute.
        If the path is absolute, there is no problem when can try to load it directly
        If the path is relative, we need to test the get the full path of the file in the following order:
            - from the current directory where kalliope has been called. Eg: /home/me/Documents/kalliope_config
            - from /etc/kalliope
            - from the root of the project. Eg: /usr/local/lib/python2.7/dist-packages/kalliope-version/kalliope/<file_path>

        :return: absolute path
        """
        return Utils.get_real_file_path(file_path)
