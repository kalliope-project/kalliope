import os

import logging
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

        if self.action == "install":
            self.install()

    def install(self):
        """
        Neuron installation method
        :return:
        """
        # clone the repo
        tmp_path = self.settings.resources.neuron_folder + os.sep + TMP_GIT_FOLDER
        Utils.print_info("Cloning repository...")
        Repo.clone_from(self.git_url, tmp_path)

        # get the dna file
        Utils.print_info("Checking DNA")
        dna_file_path = tmp_path + os.sep + DNA_FILE_NAME
        if os.path.exists(dna_file_path):
            dna_file = YAMLLoader().get_config(dna_file_path)
            logger.debug("[ResourcesManager] DNA file content: " + str(dna_file))

            if "neuron_name" not in dna_file:
                Utils.print_danger("The DNA of the neuron does not contains a \"neuron_name\"")
                os.remove(tmp_path)
            else:
                # rename the folder
                new_absolute_neuron_path = self.settings.resources.neuron_folder + os.sep + dna_file["neuron_name"].lower()
                os.rename(tmp_path, new_absolute_neuron_path)

                # check install file exists
                install_file_path = new_absolute_neuron_path + os.sep + INSTALL_FILE_NAME
                if os.path.exists(install_file_path):
                    ansible_neuron_parameters = {
                        "task_file": install_file_path
                    }
                    neuron = Neuron(name="ansible_playbook", parameters=ansible_neuron_parameters)
                    NeuronLauncher.start_neuron(neuron)
                else:
                    Utils.print_danger("Missing %s file in %s" % (INSTALL_FILE_NAME, install_file_path))

        else:
            Utils.print_danger("Missing %s file" % DNA_FILE_NAME)

