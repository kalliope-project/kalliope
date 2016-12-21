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

TMP_GIT_FOLDER = "kalliope_new_module_temp_name"
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
        self.install_file_path = self.tmp_path + os.sep + INSTALL_FILE_NAME
        self.dna_file = None

        if self.action == "install":
            self.install()

    def install(self):
        """
        Module installation method
        :return:
        """
        if self.is_settings_ok(resources=self.settings.resources,
                               folder_path=self.settings.resources.neuron_folder):
            # first, we clone the repo
            self._clone_repo(path=self.tmp_path,
                             git_url=self.git_url)

            # check the content of the cloned repo
            if self.is_repo_ok(dna_file_path=self.dna_file_path,
                               install_file_path=self.install_file_path):

                # Load the dna.yml file
                self._set_dna_file()
                if self._check_dna(dna_file=self.dna_file,
                                   tmp_path=self.tmp_path):

                    # let's move the tmp folder in the right folder and get a new path for the module
                    module_name = self.dna_file["name"].lower()
                    target_path = self._rename_temp_folder(name=module_name,
                                                           target_folder=self.settings.resources.neuron_folder,
                                                           tmp_path=self.tmp_path)

                    # if the target_path exists, then run the install file within the new repository
                    if target_path is not None:
                        self.install_file_path = target_path + os.sep + INSTALL_FILE_NAME
                        self.run_ansible_playbook_module(install_file_path=self.install_file_path)
                        Utils.print_success("Neuron %s installed" % module_name)

    def _set_dna_file(self):
        """
        load the dna file from the module.
        :return: set loading
        """
        # get the content of the DNA file
        self.dna_file = YAMLLoader().get_config(self.dna_file_path)
        logger.debug("[ResourcesManager] DNA file content: " + str(self.dna_file))


    @staticmethod
    def _check_dna(dna_file, tmp_path):
        """
        Check the dna_file values
        :param dna_file: the dna_file to check
        :param tmp_path: the temporary file path of the repo
        :return: True if ok, False otherwise
        """
        success_loading = True
        if "name" not in dna_file:
            Utils.print_danger("The DNA of does not contains a \"name\" tag")
            shutil.rmtree(tmp_path)
            success_loading = False
        return success_loading

    @staticmethod
    def is_settings_ok(resources, folder_path):
        """
        Test if required settings files in config of Kalliope are ok.
        :param resources: the Resources model
        :param folder_path: the folder associate to the resource
        :return:
        """
        settings_ok = True
        if resources is None:
            message = "Resources folder not set in settings, cannot install."
            logger.debug(message)
            Utils.print_danger(message)
            settings_ok = False

        if folder_path is None:
            message = "No folder %s set in settings, cannot install." % folder_path
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
        repo_ok = True
        # check that a install.yml file is present
        if not os.path.exists(install_file_path):
            Utils.print_danger("Missing %s file" % INSTALL_FILE_NAME)
            repo_ok = False

        Utils.print_info("Checking repository...")
        if not os.path.exists(dna_file_path):
            Utils.print_danger("Missing %s file" % DNA_FILE_NAME)
            repo_ok = False

        return repo_ok

    @staticmethod
    def _clone_repo(path, git_url):
        """
        Use git to clone locally the neuron in a temp folder
        :return:
        """
        # clone the repo
        logger.debug("GIT clone into folder: %s" % path)
        Utils.print_info("Cloning repository...")
        # if the folder already exist we remove it
        if os.path.exists(path):
            shutil.rmtree(path)
        Repo.clone_from(git_url, path)

    @staticmethod
    def _rename_temp_folder(name, target_folder, tmp_path):
        """
        Rename the temp folder of the cloned repo
        Return the name of the path to install
        :return: path to install, None if already exists
        """

        new_absolute_neuron_path = target_folder + os.sep + name
        try:
            os.rename(tmp_path, new_absolute_neuron_path)
            return new_absolute_neuron_path
        except OSError:
            # the folder already exist
            Utils.print_warning("The module %s already exist in the path %s" % (name, target_folder))
            # remove the cloned repo
            shutil.rmtree(tmp_path)


    @staticmethod
    def run_ansible_playbook_module(install_file_path):
        """
        Run the install.yml file through an Ansible playbook using the dedicated neuron !

        :param install_file_path: the path of the Ansible playbook to run.
        :param target_path:
        :param name:
        :return:
        """
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

