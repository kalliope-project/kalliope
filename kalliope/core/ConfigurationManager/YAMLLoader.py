import logging
import os

import yaml

logging.basicConfig()
logger = logging.getLogger("kalliope")


class YAMLFileNotFound(Exception):
    """
    YAML file has not been found
    """
    pass


class YAMLLoader:
    """
    Simple Class to Verify / Load a YAML file.
    """

    def __init__(self):
        pass

    @classmethod
    def get_config(cls, yaml_file):
        """
        Return the provided YAML configuration file

        :param yaml_file: The path of the configuration file
        :type yaml_file: String
        :return: the configuration file
        :rtype: String

        :Example:

            YAMLLoader.get_config(brain_file_path)

        .. seealso::  SettingLoader, BrainLoader
        .. raises:: YAMLFileNotFound
        .. warnings:: Class Method and Public
        """

        cls.file_path_to_load = yaml_file
        logger.debug("File path to load: %s " % cls.file_path_to_load)
        if os.path.isfile(cls.file_path_to_load):
            inc_import = IncludeImport(cls.file_path_to_load)
            data = inc_import.get_data()
            return data
        else:
            raise YAMLFileNotFound("File %s not found" % cls.file_path_to_load)


class IncludeImport(object):
    """
    This class manages the Include Import statement in the brain.yml file
    """

    def __init__(self, file_path):
        """
        Load yaml file, with includes statement
        :param file_path: path to the yaml file to load
        """
        # get the parent dir. will be used in case of relative path
        parent_dir = os.path.normpath(file_path + os.sep + os.pardir)

        # load the yaml file
        self.data = yaml.load(open(file_path, 'r'))

        # add included brain
        if isinstance(self.data, list):
            for el in self.data:
                if "includes" in el:
                    for inc in el["includes"]:
                        # if the path is relative, we add the root path
                        if not os.path.isabs(inc):  # os.path.isabs returns True if the path is absolute
                            # logger.debug("File path %s is relative, adding the root path" % inc)
                            inc = os.path.join(parent_dir, inc)
                            # logger.debug("New path: %s" % inc)
                        self.update(yaml.load(open(inc)))

    def get_data(self):
        """
        :return: the data for the IncludeImport
        """
        return self.data

    def update(self, data_to_add):
        """
        Method to Add an other Include statement to the original brain.yml file
        :param data_to_add: the data to add to the current brain.yml, provided by an Include Statement
        """

        # we add each synapse inside the extended brain into the main brain data
        if data_to_add is not None:
            for el in data_to_add:
                self.data.append(el)

