import inspect
import logging
import os
from six import with_metaclass
import six

from kalliope.core.Models.Signal import Signal
from .YAMLLoader import YAMLLoader
from kalliope.core.Utils import Utils
from kalliope.core.ConfigurationManager import SettingLoader
from kalliope.core.ConfigurationManager.ConfigurationChecker import ConfigurationChecker
from kalliope.core.Models import Singleton
from kalliope.core.Models.Brain import Brain
from kalliope.core.Models.Neuron import Neuron
from kalliope.core.Models.Synapse import Synapse

logging.basicConfig()
logger = logging.getLogger("kalliope")

FILE_NAME = "brain.yml"


class BrainNotFound(Exception):
    pass


class BrainLoader(with_metaclass(Singleton, object)):
    """
    This Class is used to get the brain YAML and the Brain as an object
    """

    def __init__(self, file_path=None):
        sl = SettingLoader()
        self.settings = sl.settings

        self.file_path = file_path
        if self.file_path is None:  # we don't provide a file path, so search for the default one
            self.file_path = Utils.get_real_file_path(FILE_NAME)
        else:
            self.file_path = Utils.get_real_file_path(file_path)
        # if the returned file path is none, the file doesn't exist
        if self.file_path is None:
            raise BrainNotFound("brain file not found")
        self.yaml_config = self.get_yaml_config()
        self.brain = self.load_brain()

    def get_yaml_config(self):
        """
        Class Methods which loads default or the provided YAML file and return it as a String
        :return: The loaded brain YAML
        :rtype: String

        :Example:
            brain_yaml = BrainLoader.get_yaml_config(/var/tmp/brain.yml)

        .. warnings:: Class Method
        """
        if self.file_path is None:
            brain_file_path = self._get_root_brain_path()
        else:
            brain_file_path = self.file_path
        return YAMLLoader.get_config(brain_file_path)

    def load_brain(self):
        """
        Class Methods which loads default or the provided YAML file and return a Brain
        :return: The loaded Brain
        :rtype: Brain

        :Example:

            brain = BrainLoader.load_brain(file_path="/var/tmp/brain.yml")

        .. seealso:: Brain
        .. warnings:: Class Method
        """

        # Instantiate a brain
        brain = Brain()

        # get the brain with dict
        dict_brain = self.get_yaml_config()

        brain.brain_yaml = dict_brain
        # create list of Synapse
        synapses = list()
        for synapses_dict in dict_brain:
            if "includes" not in synapses_dict:     # we don't need to check includes as it's not a synapse
                if ConfigurationChecker().check_synape_dict(synapses_dict):
                    name = synapses_dict["name"]
                    neurons = self._get_neurons(synapses_dict["neurons"], self.settings)
                    signals = self._get_signals(synapses_dict["signals"])
                    new_synapse = Synapse(name=name, neurons=neurons, signals=signals)
                    synapses.append(new_synapse)
        brain.synapses = synapses
        if self.file_path is None:
            brain.brain_file = self._get_root_brain_path()
        else:
            brain.brain_file = self.file_path
        # check that no synapse have the same name than another
        if not ConfigurationChecker().check_synapes(synapses):
            brain = None

        return brain

    @classmethod
    def _get_neurons(cls, neurons_dict, settings):
        """
        Get a list of Neuron object from a neuron dict

        :param neurons_dict: Neuron name or dictionary of Neuron_name/Neuron_parameters
        :type neurons_dict: String or dict
        :param settings:  The Settings with the global variables
        :return: A list of Neurons
        :rtype: List

        :Example:

            neurons = cls._get_neurons(synapses_dict["neurons"])

        .. seealso:: Neuron
        .. warnings:: Static and Private
        """

        neurons = list()
        for neuron_dict in neurons_dict:
            if ConfigurationChecker().check_neuron_dict(neuron_dict):
                if isinstance(neuron_dict, dict):
                    for neuron_name in neuron_dict:
                        new_neuron = Neuron(name=neuron_name, parameters=neuron_dict[neuron_name])
                        neurons.append(new_neuron)
                else:
                    new_neuron = Neuron(name=neuron_dict)
                    neurons.append(new_neuron)
        return neurons

    @classmethod
    def _get_signals(cls, signals_dict):
        """
        Get a list of Signal object from a signals dict

        :param signals_dict: Signal name or dictionary of Signal_name/Signal_parameters
        :type signals_dict: String or dict
        :return: A list of Event and/or Order
        :rtype: List

        :Example:

            signals = cls._get_signals(synapses_dict["signals"])

        .. seealso:: Event, Order
        .. warnings:: Class method and Private
        """
        signals = list()
        for signal_dict in signals_dict:
            if ConfigurationChecker().check_signal_dict(signal_dict):
                for signal_name in signal_dict:
                    new_signal = Signal(name=signal_name, parameters=signal_dict[signal_name])
                    signals.append(new_signal)

        return signals

    @staticmethod
    def _get_root_brain_path():
        """
        Return the full path of the default brain file

        :Example:

            brain.brain_file = cls._get_root_brain_path()

        .. raises:: IOError
        .. warnings:: Static method and Private
        """

        # get current script directory path. We are in /an/unknown/path/kalliope/core/ConfigurationManager
        cur_script_directory = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        # get parent dir. Now we are in /an/unknown/path/kalliope
        parent_dir = os.path.normpath(cur_script_directory + os.sep + os.pardir + os.sep + os.pardir)
        brain_path = parent_dir + os.sep + "brain.yml"
        logger.debug("Real brain.yml path: %s" % brain_path)
        if os.path.isfile(brain_path):
            return brain_path
        raise IOError("Default brain.yml file not found")
