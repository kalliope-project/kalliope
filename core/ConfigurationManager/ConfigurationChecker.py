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


class ConfigurationChecker:

    def __init__(self):
        pass

    @staticmethod
    def check_synape_dict(synape_dict):

        if 'name' not in synape_dict:
            raise NoSynapeName("The Synapse does not have a name: %s" % synape_dict)

        if 'neurons' not in synape_dict:
            raise NoSynapeNeurons("The Synapse does not have neurons: %s" % synape_dict)

        if 'signals' not in synape_dict:
            raise NoSynapeSignals("The Synapse does not have signals: %s" % synape_dict)

        return True

    @staticmethod
    def check_neuron_dict(neuron_dict):
        # TODO check that the Neuron plugin exist
        return True

    @staticmethod
    def check_signal_dict(signal_dict):
        if ('event' not in signal_dict) and ('order' not in signal_dict):
            raise NoValidSignal("The signal is not an event or an order %s" % signal_dict)
        return True

    @staticmethod
    def check_event_dict(event_dict):
        # if 'id' not in event_dict:
        #     raise NoEventID("Event must contain a unique ID: %s" % event_dict)
        if 'period' not in event_dict:
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
        Check the synapse list is ok. No double same name
        :param synapses_list:
        :type synapses_list: list of Synapse
        :return:
        """
        # TODO: check no same name
        pass
