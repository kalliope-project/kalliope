import getpass
import os

import logging

import shutil
from git import Repo
from kalliope.core.Models import Neuron

from kalliope import Utils
from kalliope.core.ConfigurationManager import YAMLLoader
from kalliope.core.ConfigurationManager import SettingLoader
from kalliope.core.NeuronLauncher import NeuronLauncher

logging.basicConfig()
logger = logging.getLogger("kalliope")

TMP_GIT_FOLDER = "kalliope_new_neuron_temp_name"
DNA_FILE_NAME = "dna.yml"
INSTALL_FILE_NAME = "install.yml"


class ResourcesManager(object):
    def __init__(self, action, **kwargs):
        super(ResourcesManager, self).__init__()
        # get settings
        sl = SettingLoader()
        self.settings = sl.settings

        # action to perform (delete, install, update)
        self.action = action

        # in case of update or install, url where
        self.git_url = kwargs.get('git_url', None)

        # temp path where we install the new module
        self.tmp_path = self.settings.resources.neuron_folder + os.sep + TMP_GIT_FOLDER
        self.dna_file_path = self.tmp_path + os.sep + DNA_FILE_NAME
        self.dna_file = None

        if self.action == "install":
            self.install()

    def install(self):
        """
        Neuron installation method
        :return:
        """
        if self.is_settings_ok():
            # first, we clone the repo
            self._clone_repo()

            # check the content of the cloned repo
            if self.is_neuron_ok():
                self.install_neuron()

    def is_settings_ok(self):
        """
        To be able to install a neuron, the user must has configured his settings
        :return: True if settings are ok
        """
        if self.settings.resources is None:
            message = "Resources folder not set in settings, cannot install a community neuron"
            logger.debug(message)
            Utils.print_danger(message)
            return False

        if self.settings.resources.neuron_folder is None:
            message = "No neuron folder set in settings, cannot install a community neuron"
            logger.debug(message)
            Utils.print_danger(message)
            return False

        return True

    def is_neuron_ok(self):
        """
        Check if the git cloned repo is fine to be installed
        :return:
        """
        Utils.print_info("Checking repository...")
        if not os.path.exists(self.dna_file_path):
            Utils.print_danger("Missing %s file" % DNA_FILE_NAME)
            return False

        # get the content of the DNA file
        self.dna_file = YAMLLoader().get_config(self.dna_file_path)
        logger.debug("[ResourcesManager] DNA file content: " + str(self.dna_file))
        if "neuron_name" not in self.dna_file:
            Utils.print_danger("The DNA of the neuron does not contains a \"neuron_name\" tag")
            os.remove(self.tmp_path)
            return False

        # check that a install.yml file is present
        install_file_path = self.tmp_path + os.sep + INSTALL_FILE_NAME
        if not os.path.exists(install_file_path):
            Utils.print_danger("Missing %s file" % DNA_FILE_NAME)
            return False

        return True

    def _clone_repo(self):
        """
        Use git to clone locally the neuron in a temp folder
        :return:
        """
        # clone the repo
        logger.debug("GIT clone into folder: %s" % self.tmp_path)
        Utils.print_info("Cloning repository...")
        # if the folder already exist we remove it
        if os.path.exists(self.tmp_path):
            shutil.rmtree(self.tmp_path)
        Repo.clone_from(self.git_url, self.tmp_path)

    def _rename_temp_neuron_folder(self):
        """
        Rename the temp folder of the cloned neuron
        Return the name of the path of the neuron to install
        :return: path of the neuron
        """
        neuron_name = self.dna_file["neuron_name"].lower()
        new_absolute_neuron_path = self.settings.resources.neuron_folder + os.sep + neuron_name
        try:
            os.rename(self.tmp_path, new_absolute_neuron_path)
            return new_absolute_neuron_path
        except OSError:
            # the folder already exist
            Utils.print_warning("The neuron %s already exist in the resource directory" % neuron_name)
            # remove the cloned repo
            shutil.rmtree(self.tmp_path)

    def install_neuron(self):
        # rename the folder
        new_neuron_path = self._rename_temp_neuron_folder()
        install_file_path = new_neuron_path + os.sep + INSTALL_FILE_NAME
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
        Utils.print_success("Neuron %s installed" % self.dna_file["neuron_name"])
