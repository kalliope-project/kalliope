import re

from core.Utils import ModuleNotFoundError


class InvalidSynapeName(Exception):
    pass


class NoSynapeName(Exception):
    pass


class NoSynapeNeurons(Exception):
    pass


class NoSynapeSignals(Exception):
    pass


class NoValidSignal(Exception):
    pass


class NoEventID(Exception):
    pass


class NoEventPeriod(Exception):
    pass


class MultipleSameSynapseName(Exception):
    pass


class NotValidSynapseName(Exception):
    pass


class ConfigurationChecker:

    def __init__(self):
        pass

    @staticmethod
    def check_synape_dict(synape_dict):

        if 'name' not in synape_dict:
            raise NoSynapeName("The Synapse does not have a name: %s" % synape_dict)

        # check that the name is conform
        # Regex for [a - zA - Z0 - 9\-] with dashes allowed in between but not at the start or end
        pattern = r'(?=[a-zA-Z0-9\-]{4,100}$)^[a-zA-Z0-9]+(\-[a-zA-Z0-9]+)*$'
        prog = re.compile(pattern)
        result = prog.match(synape_dict["name"])
        if result is None:
            raise InvalidSynapeName("Error with synapse name \"%s\".Valid syntax: [a - zA - Z0 - 9\-] with dashes "
                                    "allowed in between but not at the start or end" % synape_dict["name"])

        if 'neurons' not in synape_dict:
            raise NoSynapeNeurons("The Synapse does not have neurons: %s" % synape_dict)

        if 'signals' not in synape_dict:
            raise NoSynapeSignals("The Synapse does not have signals: %s" % synape_dict)

        return True

    @staticmethod
    def check_neuron_dict(neuron_dict):
        """
        Check received neuron dict is valid:
        - neuron exist
        :param neuron_dict:
        :return:
        """
        def check_neuron_exist(neuron_name):
            package_name = "neurons"
            mod = __import__(package_name, fromlist=[neuron_name])
            try:
                getattr(mod, neuron_name)
            except AttributeError:
                raise ModuleNotFoundError("The module %s does not exist in package %s" % (neuron_name, package_name))
            return True

        if isinstance(neuron_dict, dict):
            for neuron_name in neuron_dict:
                check_neuron_exist(neuron_name)
        else:
            check_neuron_exist(neuron_dict)
        return True

    @staticmethod
    def check_signal_dict(signal_dict):
        if ('event' not in signal_dict) and ('order' not in signal_dict):
            raise NoValidSignal("The signal is not an event or an order %s" % signal_dict)
        return True

    @staticmethod
    def check_event_dict(event_dict):
        if event_dict is None:
            raise NoEventPeriod("Event must contain a period: %s" % event_dict)

        return True

    @staticmethod
    def check_order_dict(order_dict):
        if order_dict is not None:
            return True
        return False

    @staticmethod
    def check_synapes(synapses_list):
        """
        Check the synapse list is ok:
         - No double same name
        :param synapses_list:
        :type synapses_list: list of Synapse
        :return:
        """
        seen = set()
        for synapse in synapses_list:
            # convert ascii to UTF-8
            synapse_name = synapse.name.encode('utf-8')
            if synapse_name in seen:
                raise MultipleSameSynapseName("Multiple synapse found with the same name: %s" % synapse_name)
            seen.add(synapse.name)

        return True
