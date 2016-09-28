import os
import yaml


class YAMLFileNotFound(Exception):
    pass


class YAMLLoader:

    def __init__(self, yaml_file):
        self.file = yaml_file

    def get_config(self):
        """
        Load settings file
        :return: cfg : the configuration file
        """
        # Load settings.
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        try:
            with open(os.path.join(__location__, self.file)) as ymlfile:
                cfg = yaml.load(ymlfile)
            return cfg
        except IOError:
            raise YAMLFileNotFound("The file path %s does not exist" % self.file)
