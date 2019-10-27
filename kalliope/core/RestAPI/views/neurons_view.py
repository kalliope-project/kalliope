import glob
import inspect
import logging
import os

from flask import jsonify, Blueprint, request
from kalliope.core.ResourcesManager import ResourcesManager, ResourcesManagerException
from kalliope.core.Utils import Utils

logging.basicConfig()
logger = logging.getLogger("kalliope")

LIST_EXCLUDED_DIR_NAME = ["__pycache__"]
KALLIOPE_WEBSITE_NEURON_URL = "https://raw.githubusercontent.com/kalliope-project/kalliope-project.github.io/" \
                              "sources/_data/community_neurons.yml"


class NeuronsView(Blueprint):
    def __init__(self, name, import_name, app=None, brain=None, settings=None):
        self.brain = brain
        self.settings = settings
        self.app = app
        super(NeuronsView, self).__init__(name, import_name)

        # routes
        self.add_url_rule('/neurons', view_func=self.get_neurons, methods=['GET'])
        self.add_url_rule('/neurons/install', view_func=self.install_resource_by_git_url, methods=['POST'])

    def get_neurons(self):
        """
        list all installed neuron

        curl -i --user admin:secret -X GET http://127.0.0.1:5000/neurons
        :return:
        """
        data = {
            "core": self._get_list_core_neuron(),
            "community": self._get_list_installed_community_neuron()
        }
        logger.debug("[FlaskAPI] get_neurons: all")
        data = jsonify(data)
        return data, 200

    @staticmethod
    def install_resource_by_git_url():
        """
        Install a new resource from the given git URL. Call the resource manager

        curl -i -H "Content-Type: application/json" \
        --user admin:secret \
        -X POST \
        -d '
        {
            "git_url": "https://github.com/kalliope-project/kalliope_neuron_wikipedia.git",
            "sudo_password": "azerty"  # TODO add kalliope to sudoer file and remove this
        }
        ' \
        http://127.0.0.1:5000/neurons/install
        """
        if not request.get_json() or 'git_url' not in request.get_json():
            data = {
                "Error": "Wrong parameters, 'git_url' not set"
            }
            return jsonify(error=data), 400

        parameters = {
            "git_url": request.get_json()["git_url"],
            "sudo_password": request.get_json()["sudo_password"]
        }
        res_manager = ResourcesManager(**parameters)
        try:
            dna = res_manager.install()
        except ResourcesManagerException as e:
            data = {
                "error": "%s" % e
            }
            return jsonify(data), 400

        if dna is not None:
            return jsonify(dna.serialize()), 200
        else:
            data = {
                "Error": "Error during resource installation"
            }
            return jsonify(error=data), 400

    def _get_list_core_neuron(self):
        current_path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        kalliope_core_neuron_folder = Utils.get_current_file_parent_path(Utils.get_current_file_parent_parent_path(current_path)) + os.sep + "neurons/*"
        return self._get_neuron_name_list_from_path(kalliope_core_neuron_folder)

    def _get_list_installed_community_neuron(self):
        if self.settings.resources.neuron_folder is not None:
            return self._get_neuron_name_list_from_path(self.settings.resources.neuron_folder + os.sep + "/*")

        return list()

    @staticmethod
    def _get_neuron_name_list_from_path(neuron_path_list):
        """
        From a given path, return all folder name as list.
        E.g: /home/pi/kalliope/neurons
        Will return [wikipedia_searcher, gmail]
        :param neuron_path_list: path to the community neurons folder
        :return:
        """

        glob_neuron_path_list = glob.glob(neuron_path_list)

        neuron_name_list = list()
        for neuron_path in glob_neuron_path_list:
            if os.path.isdir(neuron_path):
                neuron_name = os.path.basename(os.path.normpath(neuron_path))
                if neuron_name not in LIST_EXCLUDED_DIR_NAME:
                    neuron_name_list.append(neuron_name)
        return neuron_name_list
