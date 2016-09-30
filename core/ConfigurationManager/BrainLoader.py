
from YAMLLoader import YAMLLoader
from core.ConfigurationManager.ConfigurationChecker import ConfigurationChecker
from core.Models.Brain import Brain
from core.Models.Event import Event
from core.Models.Neuron import Neuron
from core.Models.Order import Order
from core.Models.Synapse import Synapse

FILE_NAME = "brain.yml"


class BrainLoader(YAMLLoader):

    def __init__(self, filename=None):
        self.fileName = filename
        if filename is None:
            self.fileName = FILE_NAME
        self.filePath = "../../" + self.fileName
        YAMLLoader.__init__(self, self.filePath)

    def get_config(self):
        return YAMLLoader.get_config(self)

    def get_brain(self):
        """
        return a brain object from YAML settings
        :return: Brain object
        :rtype: Brain
        """
        # get the brain with dict
        dict_brain = self.get_config()
        # create a new brain
        brain = Brain()
        # create list of Synapse
        synapses = list()
        for synapes_dict in dict_brain:
            # print synapes_dict
            if ConfigurationChecker().check_synape_dict(synapes_dict):
                # print "synapes_dict ok"
                name = synapes_dict["name"]
                neurons = self._get_neurons(synapes_dict["neurons"])
                signals = self._get_signals(synapes_dict["signals"])
                new_synapse = Synapse(name=name, neurons=neurons, signals=signals)
                synapses.append(new_synapse)
        brain.synapes = synapses
        # check that no synapse have the same name than another
        if ConfigurationChecker().check_synapes(synapses):
            return brain
        return None

    def _get_neurons(self, neurons_dict):
        """
        Get a list of Neuron object from a neuron dict
        :param neurons_dict:
        :return:
        """
        neurons = list()
        for neuron_dict in neurons_dict:
            # print neuron_dict
            if ConfigurationChecker().check_neuron_dict(neuron_dict):
                # print "Neurons dict ok"
                for neuron_name in neuron_dict:
                    name = neuron_name
                    parameters = neuron_dict[name]
                    # print parameters
                    new_neuron = Neuron(name=name, parameters=parameters)
                    neurons.append(new_neuron)

        return neurons

    def _get_signals(self, signals_dict):
        # print signals_dict
        signals = list()
        for signal_dict in signals_dict:
            if ConfigurationChecker().check_signal_dict(signal_dict):
                # print "Signals dict ok"
                event_or_order = self._get_event_or_order_from_dict(signal_dict)
                signals.append(event_or_order)

        return signals

    @staticmethod
    def _get_event_or_order_from_dict(signal_or_event_dict):

        if 'event' in signal_or_event_dict:
            # print "is event"
            event = signal_or_event_dict["event"]
            if ConfigurationChecker.check_event_dict(event):
                return Event(period=event["period"])

        if 'order' in signal_or_event_dict:
            order = signal_or_event_dict["order"]
            if ConfigurationChecker.check_order_dict(order):
                return Order(sentence=order)


