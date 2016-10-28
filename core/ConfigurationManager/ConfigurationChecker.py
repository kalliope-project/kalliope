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

    """

        This Class provides all method to Check the configuration files are properly set up.
    """

    def __init__(self):
        pass

    @staticmethod
    def check_synape_dict(synape_dict):
        """

        Return True if the provided dict is well corresponding to a Synapse

        :param synape_dict: The synapse Dictionary
        :type synape_dict: Dict
        :return: True if synapse are ok
        :rtype: Boolean

        :Example:

            ConfigurationChecker().check_synape_dict(synapses_dict):

        .. seealso:: Synapse
        .. raises:: NoSynapeName, InvalidSynapeName, NoSynapeNeurons, NoSynapeSignals
        .. warnings:: Static and Public
        """

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

        :param neuron_dict: The neuron Dictionary
        :type neuron_dict: Dict
        :return: True if neuron is ok
        :rtype: Boolean

        :Example:

            ConfigurationChecker().check_neuron_dict(neurons_dict):

        .. seealso:: Synapse
        .. raises:: ModuleNotFoundError
        .. warnings:: Static and Public
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
        """

        Check received signal dictionary is valid:

        :param signal_dict: The signal Dictionary
        :type signal_dict: Dict
        :return: True if signal are ok
        :rtype: Boolean

        :Example:

            ConfigurationChecker().check_signal_dict(signal_dict):

        .. seealso:: Order, Event
        .. raises:: NoValidSignal
        .. warnings:: Static and Public
        """

        if ('event' not in signal_dict) and ('order' not in signal_dict):
            raise NoValidSignal("The signal is not an event or an order %s" % signal_dict)
        return True

    @staticmethod
    def check_event_dict(event_dict):
        """

        Check received event dictionary is valid:

        :param event_dict: The event Dictionary
        :type event_dict: Dict
        :return: True if event are ok
        :rtype: Boolean

        :Example:

            ConfigurationChecker().check_event_dict(event_dict):

        .. seealso::  Event
        .. raises:: NoEventPeriod
        .. warnings:: Static and Public
        """

        if event_dict is None:
            raise NoEventPeriod("Event must contain a period: %s" % event_dict)

        return True

    @staticmethod
    def check_order_dict(order_dict):
        """

        Check received order dictionary is valid:

        :param order_dict: The Order Dict
        :type order_dict: Dict
        :return: True if event are ok
        :rtype: Boolean

        :Example:

            ConfigurationChecker().check_order_dict(order_dict):

        .. seealso::  Order
        .. raises:: NoEventPeriod
        .. warnings:: Static and Public
        """

        if order_dict is not None:
            return True
        return False

    @staticmethod
    def check_synapes(synapses_list):
        """

        Check the synapse list is ok:
            - No double same name

        :param synapses_list: The Synapse List
        :type synapses_list: List
        :return: list of Synapse
        :rtype: List

        :Example:

            ConfigurationChecker().check_synapes(order_dict):

        .. seealso::  Synapse
        .. raises:: MultipleSameSynapseName
        .. warnings:: Static and Public
        """


        seen = set()
        for synapse in synapses_list:
            # convert ascii to UTF-8
            synapse_name = synapse.name.encode('utf-8')
            if synapse_name in seen:
                raise MultipleSameSynapseName("Multiple synapse found with the same name: %s" % synapse_name)
            seen.add(synapse.name)

        return True
