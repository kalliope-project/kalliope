import inspect
import logging
import os
import time
import glob
from flask import jsonify, Blueprint
from flask import request
from werkzeug.utils import secure_filename

from kalliope import Utils
from kalliope.core.ConfigurationManager import BrainLoader, SettingEditor
from kalliope.core.ConfigurationManager.ConfigurationChecker import KalliopeModuleNotFoundError, ConfigurationChecker, \
    InvalidSynapeName, NoSynapeNeurons, NoSynapeSignals
from kalliope.core.Lifo.LifoManager import LifoManager
from kalliope.core.Models import Synapse
from kalliope.core.Models.MatchedSynapse import MatchedSynapse
from kalliope.core.OrderListener import OrderListener
from kalliope.core.RestAPI import utils
from kalliope.core.RestAPI.utils import requires_auth
from kalliope.core.SynapseLauncher import SynapseLauncher

logging.basicConfig()
logger = logging.getLogger("kalliope")

LIST_EXCLUDED_DIR_NAME = ["__pycache__"]


class NeuronsView(Blueprint):
    def __init__(self, name, import_name, app=None, brain=None, settings=None):
        self.brain = brain
        self.settings = settings
        self.app = app
        super().__init__(name, import_name)

        # routes
        self.add_url_rule('/neurons', view_func=self.get_neurons, methods=['GET'])

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

        glob_neuron_path_list = glob.glob(neuron_path_list)

        neuron_name_list = list()
        for neuron_path in glob_neuron_path_list:
            if os.path.isdir(neuron_path):
                neuron_name = os.path.basename(os.path.normpath(neuron_path))
                if neuron_name not in LIST_EXCLUDED_DIR_NAME:
                    neuron_name_list.append(neuron_name)
        return neuron_name_list
