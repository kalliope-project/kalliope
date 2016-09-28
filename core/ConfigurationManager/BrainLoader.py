
from YAMLLoader import YAMLLoader
from core.ConfigurationManager.ConfigurationChecker import ConfigurationChecker
from core.Models.Brain import Brain
from core.Models.Event import Event
from core.Models.Neurone import Neurone
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

    def get_events(self):
        events_in_brain = list()
        for el in self.get_config():
            whens = el["when"]
            for when in whens:
                # if key event exist in when of the task
                if 'event' in when:
                    events_in_brain.append(when['event'])

        return events_in_brain

    def get_brain(self):
        # get the brain with dict
        dict_brain = self.get_config()
        # create a new brain
        brain = Brain()
        # create list of Synapse
        synapses = list()
        for synapes_dict in dict_brain:
            print synapes_dict
            if ConfigurationChecker().check_synape_dict(synapes_dict):
                print "synapes_dict ok"
                name = synapes_dict["name"]
                neurons = self._get_neurons(synapes_dict["neurons"])
                signals = self._get_signals(synapes_dict["signals"])
                new_synapse = Synapse(name=name, neurons=neurons, signals=signals)
                synapses.append(new_synapse)

    def _get_neurons(self, neurons_dict):
        """
        Get a list of Neuron object from a neuron dict
        :param neurons_dict:
        :return:
        """
        neurons = list()
        for neuron_dict in neurons_dict:
            print neuron_dict
            if ConfigurationChecker().check_neuron_dict(neuron_dict):
                print "Neurons dict ok"
            for neuron_name in neuron_dict:
                name = neuron_name
                parameters = neuron_dict[name]
                # print parameters
                new_neuron = Neurone(name=name, parameters=parameters)
                neurons.append(new_neuron)

        return neurons

    def _get_signals(self, signals_dict):
        print signals_dict
        signals = list()
        for signal_dict in signals_dict:
            if ConfigurationChecker().check_signal_dict(signal_dict):
                print "Signals dict ok"
                event_or_oder = self._get_event_or_order_from_dict(signal_dict)

        return signals

    @staticmethod
    def _get_event_or_order_from_dict(signal_or_event_dict):

        if 'event' in signal_or_event_dict:
            print "is event"
            event = signal_or_event_dict["event"]
            if ConfigurationChecker.check_event_dict(event):
                return Event(identifier=event["id"], period=event["period"])

        if 'order' in signal_or_event_dict:
            print "is order"
            if ConfigurationChecker.check_order_dict(signal_or_event_dict["order"]):
                return Order(signal_or_event_dict["order"])


