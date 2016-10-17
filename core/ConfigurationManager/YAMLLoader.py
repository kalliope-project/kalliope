import logging
import os
import yaml

from core.Utils import Utils

logging.basicConfig()
logger = logging.getLogger("kalliope")


class YAMLFileNotFound(Exception):
    pass


class YAMLLoader:

    def __init__(self):
        pass

    @classmethod
    def get_config(cls, yaml_file):
        """
        Load settings file
        :return: cfg : the configuration file
        """
        # # Load settings.
        # __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        # try:
        #     with open(os.path.join(__location__, yaml_file)) as ymlfile:
        #         cfg = yaml.load(ymlfile)
        #     return cfg
        # except IOError:
        #     raise YAMLFileNotFound("The file path %s does not exist" % yaml_file)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        logger.debug("Current dir: %s " % current_dir)
        root_dir = os.path.join(current_dir, "../../")
        root_dir = os.path.normpath(root_dir)
        logger.debug("Root dir: %s " % root_dir)
        file_path_to_load = os.path.join(root_dir, yaml_file)
        logger.debug("File path to load: %s " % file_path_to_load)
        if os.path.isfile(yaml_file):
            data = IncludeLoader(open(file_path_to_load, 'r')).get_data()
            # print Utils.print_yaml_nicely(data)
            return data
        else:
            raise YAMLFileNotFound("File %s not found" % file_path_to_load)


class IncludeLoader(yaml.Loader):

    def __init__(self, *args, **kwargs):
        super(IncludeLoader, self).__init__(*args, **kwargs)
        self.add_constructor('!include', self._include)
        if 'root' in kwargs:
            self.root = kwargs['root']
        elif isinstance(self.stream, file):
            self.root = os.path.dirname(self.stream.name)
        else:
            self.root = os.path.curdir

    def _include(self, loader, node):
        oldRoot = self.root
        filename = os.path.join(self.root, loader.construct_scalar(node))
        self.root = os.path.dirname(filename)
        data = yaml.load(open(filename, 'r'))
        self.root = oldRoot
        return data