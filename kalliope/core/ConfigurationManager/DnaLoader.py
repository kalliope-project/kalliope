from kalliope.core import Utils
from kalliope.core.ConfigurationManager import YAMLLoader
from kalliope.core.Models.Dna import Dna


class InvalidDNAException(Exception):
    pass

VALID_DNA_MODULE_TYPE = ["neuron", "stt", "tts", "trigger"]


class DnaLoader(object):

    def __init__(self, file_path):
        """
        Load a DNA file and check the content of this one
        :param file_path: path the the DNA file to load
        """
        self.file_path = file_path
        if self.file_path is None:
            raise InvalidDNAException("[DnaLoader] You must set a file file")

        self.yaml_config = YAMLLoader.get_config(self.file_path)
        self.dna = self._load_dna()

    def get_yaml_config(self):
        """
        Class Methods which loads default or the provided YAML file and return it as a String
        :return: The loaded DNA YAML file
        :rtype: String
        """
        return self.yaml_config

    def get_dna(self):
        """
        Return the loaded DNA object if this one is valid
        :return:
        """
        return self.dna

    def _load_dna(self):
        """
        retur a DNA object from a loaded yaml file
        :return:
        """
        new_dna = None
        if self._check_dna_file(self.yaml_config):
            new_dna = Dna()
            new_dna.name = self.yaml_config["name"]
            new_dna.module_type = self.yaml_config["type"]
            new_dna.author = self.yaml_config["author"]
            new_dna.kalliope_supported_version = self.yaml_config["kalliope_supported_version"]
            new_dna.tags = self.yaml_config["tags"]

        return new_dna

    @staticmethod
    def _check_dna_file(dna_file):
        """
        Check the content of a DNA file
        :param dna_file: the dna to check
        :return: True if ok, False otherwise
        """
        success_loading = True
        if "name" not in dna_file:
            Utils.print_danger("The DNA of does not contains a \"name\" tag")
            success_loading = False

        if "type" not in dna_file:
            Utils.print_danger("The DNA of does not contains a \"type\" tag")
            success_loading = False

        else:
            # we have a type, check that is a valid one
            if dna_file["type"] not in VALID_DNA_MODULE_TYPE:
                Utils.print_danger("The DNA type %s is not valid" % dna_file["type"])
                Utils.print_danger("The DNA type must be one of the following: %s" % VALID_DNA_MODULE_TYPE)
                success_loading = False

        if "kalliope_supported_version" not in dna_file:
            Utils.print_danger("The DNA of does not contains a \"kalliope_supported_version\" tag")
            success_loading = False
        else:
            # kalliope_supported_version must be a non empty list
            if not isinstance(dna_file["kalliope_supported_version"], list):
                Utils.print_danger("kalliope_supported_version is not a list")
                success_loading = False
            else:
                if not dna_file["kalliope_supported_version"]:
                    Utils.print_danger("kalliope_supported_version cannot be empty")
                    success_loading = False

        return success_loading
