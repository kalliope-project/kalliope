import inspect
import logging
import os

from YAMLLoader import YAMLLoader
from kalliope.core.Utils import Utils
from kalliope.core.ConfigurationManager.ConfigurationChecker import ConfigurationChecker
from kalliope.core.Models import Singleton
from kalliope.core.Models.Brain import Brain
from kalliope.core.Models.Event import Event
from kalliope.core.Models.Neuron import Neuron
from kalliope.core.Models.Order import Order
from kalliope.core.Models.Synapse import Synapse

logging.basicConfig()
logger = logging.getLogger("kalliope")

FILE_NAME = "brain.yml"


class BrainNotFound(Exception):
    pass


class BrainLoader(object):
    """
    This Class is used to get the brain YAML and the Brain as an object
    """
    __metaclass__ = Singleton

    def __init__(self, file_path=None):
        self.file_path = file_path
        if self.file_path is None:  # we don't provide a file path, so search for the default one
            self.file_path = Utils.get_real_file_path(FILE_NAME)
        else:
            self.file_path = Utils.get_real_file_path(file_path)
        # if the returned file path is none, the file doesn't exist
        if self.file_path is None:
            raise BrainNotFound("brain file not found")
        self.yaml_config = self.get_yaml_config()
        self.brain = self.get_brain()

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

    def get_brain(self):
        """
        Class Methods which loads default or the provided YAML file and return a Brain
        :return: The loaded Brain
        :rtype: Brain

        :Example:

            brain = BrainLoader.get_brain(file_path="/var/tmp/brain.yml")

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
                    # print "synapses_dict ok"
                    name = synapses_dict["name"]
                    neurons = self._get_neurons(synapses_dict["neurons"])
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

    @staticmethod
    def _get_neurons(neurons_dict):
        """
        Get a list of Neuron object from a neuron dict

        :param neurons_dict: Neuron name or dictionary of Neuron_name/Neuron_parameters
        :type neurons_dict: String or dict
        :return: A list of Neurons
        :rtype: List

        :Example:

            neurons = cls._get_neurons(synapses_dict["neurons"])

        .. seealso:: Neuron
        .. warnings:: Static and Private
        """

        neurons = list()
        for neuron_dict in neurons_dict:
            if isinstance(neuron_dict, dict):
                if ConfigurationChecker().check_neuron_dict(neuron_dict):
                    # print "Neurons dict ok"
                    for neuron_name in neuron_dict:

                        name = neuron_name
                        parameters = neuron_dict[name]
                        # print parameters
                        new_neuron = Neuron(name=name, parameters=parameters)
                        neurons.append(new_neuron)
            else:
                # the neuron does not have parameter
                if ConfigurationChecker().check_neuron_dict(neuron_dict):
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
        # print signals_dict
        signals = list()
        for signal_dict in signals_dict:
            if ConfigurationChecker().check_signal_dict(signal_dict):
                # print "Signals dict ok"
                event_or_order = cls._get_event_or_order_from_dict(signal_dict)
                signals.append(event_or_order)

        return signals

    @classmethod
    def _get_event_or_order_from_dict(cls, signal_or_event_dict):
        """
        The signal is either an Event or an Order

        :param signal_or_event_dict: A dict of event or signal
        :type signal_or_event_dict: dict
        :return: The object corresponding to An Order or an Event
        :rtype: An Order or an Event

        :Example:

            event_or_order = cls._get_event_or_order_from_dict(signal_dict)

        .. seealso:: Event, Order
        .. warnings:: Static method and Private
        """
        if 'event' in signal_or_event_dict:
            # print "is event"
            event = signal_or_event_dict["event"]
            if ConfigurationChecker.check_event_dict(event):
                return cls._get_event_object(event)

        if 'order' in signal_or_event_dict:
            order = signal_or_event_dict["order"]
            if ConfigurationChecker.check_order_dict(order):
                return Order(sentence=order)

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

    @classmethod
    def _get_event_object(cls, event_dict):
        def get_key(key_name):
            try:
                return event_dict[key_name]
            except KeyError:
                return None

        year = get_key("year")
        month = get_key("month")
        day = get_key("day")
        week = get_key("week")
        day_of_week = get_key("day_of_week")
        hour = get_key("hour")
        minute = get_key("minute")
        second = get_key("second")

        return Event(year=year, month=month, day=day, week=week,
                     day_of_week=day_of_week, hour=hour, minute=minute, second=second)