import getpass
import logging
import os
import shutil

from git import Repo
from packaging import version

from kalliope.core.ConfigurationManager import SettingLoader
from kalliope.core.ConfigurationManager.DnaLoader import DnaLoader
from kalliope.core.Models import Neuron
from kalliope.core.NeuronLauncher import NeuronLauncher
from kalliope.core.Utils import Utils

logging.basicConfig()
logger = logging.getLogger("kalliope")

# Global values for processing:
LOCAL_TMP_FOLDER = "/tmp/kalliope/resources/"
TMP_GIT_FOLDER = "kalliope_new_module_temp_name"
DNA_FILE_NAME = "dna.yml"
INSTALL_FILE_NAME = "install.yml"

# Global values for required parameters in DNA:
DNA_NAME = "name"
DNA_TYPE = "type"

# Global_Names for 'types' to match:
TYPE_NEURON = "neuron"
TYPE_TTS = "tts"
TYPE_STT = "stt"
TYPE_TRIGGER = "trigger"


class ResourcesManagerException(Exception):
    pass


class ResourcesManager(object):
    def __init__(self, **kwargs):
        """
        This class is used to manage community resources.
        :param kwargs:
            git-url: the url of the module to clone and install
        """
        super(ResourcesManager, self).__init__()
        # get settings
        sl = SettingLoader()
        self.settings = sl.settings

        # in case of update or install, url where
        self.git_url = kwargs.get('git_url', None)

        # temp path where we install the new module
        self.tmp_path = LOCAL_TMP_FOLDER + TMP_GIT_FOLDER
        self.dna_file_path = self.tmp_path + os.sep + DNA_FILE_NAME
        self.install_file_path = self.tmp_path + os.sep + INSTALL_FILE_NAME
        self.dna = None

    def install(self):
        """
        Module installation method.
        """
        # first, we clone the repo
        self._clone_repo(path=self.tmp_path,
                         git_url=self.git_url)

        # check the content of the cloned repo
        if self.is_repo_ok(dna_file_path=self.dna_file_path,
                           install_file_path=self.install_file_path):

            # Load the dna.yml file
            self.dna = DnaLoader(self.dna_file_path).get_dna()
            if self.dna is not None:
                logger.debug("[ResourcesManager] DNA file content: " + str(self.dna))
                if self.is_settings_ok(resources=self.settings.resources, dna=self.dna):
                    # the dna file is ok, check the supported version
                    if self._check_supported_version(current_version=self.settings.kalliope_version,
                                                     supported_versions=self.dna.kalliope_supported_version):

                        # Let's find the target folder depending the type
                        module_type = self.dna.module_type.lower()
                        target_folder = self._get_target_folder(resources=self.settings.resources,
                                                                module_type=module_type)
                        if target_folder is not None:
                            # let's move the tmp folder in the right folder and get a new path for the module
                            module_name = self.dna.name.lower()
                            target_path = self._rename_temp_folder(name=self.dna.name.lower(),
                                                                   target_folder=target_folder,
                                                                   tmp_path=self.tmp_path)

                            # if the target_path exists, then run the install file within the new repository
                            if target_path is not None:
                                self.install_file_path = target_path + os.sep + INSTALL_FILE_NAME
                                self.run_ansible_playbook_module(install_file_path=self.install_file_path)
                                Utils.print_success("Module: %s installed" % module_name)
                else:
                    logger.debug("[ResourcesManager] installation cancelled, deleting temp repo %s"
                                 % str(self.tmp_path))
                    shutil.rmtree(self.tmp_path)

    @staticmethod
    def is_settings_ok(resources, dna):
        """
        Test if required settings files in config of Kalliope are ok.
        The resource object must not be empty
        Check id the use have set the an installation path in his settings for the target module type
        :param resources: the Resources model
        :param dna: DNA info about the module to install
        :return:
        """
        settings_ok = True
        if resources is None:
            message = "Resources folder not set in settings, cannot install."
            logger.debug(message)
            Utils.print_danger(message)
            settings_ok = False
        else:
            if dna.module_type == "neuron" and resources.neuron_folder is None:
                message = "Resources folder for neuron installation not set in settings, cannot install."
                logger.debug(message)
                Utils.print_danger(message)
                settings_ok = False
            if dna.module_type == "stt" and resources.stt_folder is None:
                message = "Resources folder for stt installation not set in settings, cannot install."
                logger.debug(message)
                Utils.print_danger(message)
                settings_ok = False
            if dna.module_type == "tts" and resources.tts_folder is None:
                message = "Resources folder for tts installation not set in settings, cannot install."
                logger.debug(message)
                Utils.print_danger(message)
                settings_ok = False
            if dna.module_type == "trigger" and resources.trigger_folder is None:
                message = "Resources folder for trigger installation not set in settings, cannot install."
                logger.debug(message)
                Utils.print_danger(message)
                settings_ok = False

        return settings_ok

    @staticmethod
    def is_repo_ok(dna_file_path, install_file_path):
        """
        Check if the git cloned repo is fine to be installed
        :return: True if repo is ok to be installed, False otherwise
        """
        Utils.print_info("Checking repository...")
        repo_ok = True
        # check that a install.yml file is present
        if not os.path.exists(install_file_path):
            Utils.print_danger("Missing %s file" % INSTALL_FILE_NAME)
            repo_ok = False

        if not os.path.exists(dna_file_path):
            Utils.print_danger("Missing %s file" % DNA_FILE_NAME)
            repo_ok = False

        return repo_ok

    @staticmethod
    def _get_target_folder(resources, module_type):
        """
        Return the folder from the resources and given a module type
        :param resources: Resource object
        :type resources: Resources
        :param module_type: type of the module
        :return: path of the folder
        """
        # dict to get the path behind a type of resource
        module_type_converter = {
            TYPE_NEURON: resources.neuron_folder,
            TYPE_STT: resources.stt_folder,
            TYPE_TTS: resources.tts_folder,
            TYPE_TRIGGER: resources.trigger_folder
        }
        # Let's find the right path depending of the type
        try:
            folder_path = module_type_converter[module_type]
        except KeyError:
            folder_path = None
        # No folder_path has been found
        message = "No %s folder set in settings, cannot install." % module_type
        if folder_path is None:
            logger.debug(message)
            Utils.print_danger(message)

        return folder_path

    @staticmethod
    def _clone_repo(path, git_url):
        """
        Use git to clone locally the neuron in a temp folder
        :return:
        """
        # clone the repo
        logger.debug("[ResourcesManager] GIT clone into folder: %s" % path)
        Utils.print_info("Cloning repository...")
        # if the folder already exist we remove it
        if os.path.exists(path):
            shutil.rmtree(path)
        else:
            os.makedirs(path)
        Repo.clone_from(git_url, path)

    @staticmethod
    def _rename_temp_folder(name, target_folder, tmp_path):
        """
        Rename the temp folder of the cloned repo
        Return the name of the path to install
        :return: path to install, None if already exists
        """
        logger.debug("[ResourcesManager] Rename temp folder")
        new_absolute_neuron_path = target_folder + os.sep + name
        try:
            os.rename(tmp_path, new_absolute_neuron_path)
            return new_absolute_neuron_path
        except OSError:
            # the folder already exist
            Utils.print_warning("The module %s already exist in the path %s" % (name, target_folder))
            # remove the cloned repo
            logger.debug("[ResourcesManager] Deleting temp folder %s" % str(tmp_path))
            shutil.rmtree(tmp_path)

    @staticmethod
    def run_ansible_playbook_module(install_file_path):
        """
        Run the install.yml file through an Ansible playbook using the dedicated neuron !

        :param install_file_path: the path of the Ansible playbook to run.
        :return:
        """
        logger.debug("[ResourcesManager] Run ansible playbook")
        Utils.print_info("Starting neuron installation")
        # ask the sudo password
        pswd = getpass.getpass('Sudo password:')
        ansible_neuron_parameters = {
            "task_file": install_file_path,
            "sudo": True,
            "sudo_user": "root",
            "sudo_password": pswd
        }
        neuron = Neuron(name="ansible_playbook", parameters=ansible_neuron_parameters)
        NeuronLauncher.start_neuron(neuron)

    @staticmethod
    def _check_supported_version(current_version, supported_versions):
        """
        The dna file contains supported Kalliope version for the module to install.
        Check if supported versions are match the current installed version. If not, ask the user to confirm the
        installation anyway
        :param current_version: current version installed of Kalliope. E.g 0.4.0
        :param supported_versions: list of supported version
        :return: True if the version is supported or user has confirmed the installation
        """
        logger.debug("[ResourcesManager] Current installed version of Kalliope: %s" % str(current_version))
        logger.debug("[ResourcesManager] Module supported version: %s" % str(supported_versions))

        supported_version_found = False
        for supported_version in supported_versions:
            if version.parse(current_version) == version.parse(supported_version):
                # we found the exact version
                supported_version_found = True
                break

        if not supported_version_found:
            # we ask the user if we want to install the module even if the version doesn't match
            Utils.print_info("Current installed version of Kalliope: %s" % current_version)
            Utils.print_info("Module supported versions: %s" % str(supported_versions))
            Utils.print_warning("The neuron seems to be not supported by your current version of Kalliope")
            supported_version_found = Utils.query_yes_no("install it anyway?")
            logger.debug("[ResourcesManager] install it anyway user answer: %s" % supported_version_found)

        logger.debug("[ResourcesManager] check_supported_version: %s" % str(supported_version_found))
        return supported_version_found
