import re
import os
import imp

from kalliope.core.Utils.Utils import ModuleNotFoundError
from kalliope.core.ConfigurationManager.SettingLoader import SettingLoader

class InvalidSynapeName(Exception):
    """
    The name of the synapse is not correct. It should only contains alphanumerics at the beginning and the end of
    its name. It can also contains dash in beetween alphanumerics.
    """
    pass


class NoSynapeName(Exception):
    """
    A synapse needs a name
    """
    pass


class NoSynapeNeurons(Exception):
    """
    A synapse must contains at least one neuron

    .. seealso:: Synapse, Neuron
    """
    pass


class NoSynapeSignals(Exception):
    """
    A synapse must contains at least an Event or an Order

    .. seealso:: Event, Order
    """
    pass


class NoValidSignal(Exception):
    """
    A synapse must contains at least a valid Event or an Order

    .. seealso:: Event, Order
    """

    pass


class NoEventPeriod(Exception):
    """
    An Event must contains a period corresponding to its execution

    .. seealso:: Event
    """
    pass


class MultipleSameSynapseName(Exception):
    """
    A synapse name must be unique
    """
    pass


class NoValidOrder(Exception):
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

        def check_neuron_exist(neuron_module_name):
            """
            Return True if the neuron_name python Class exist in neurons package
            :param neuron_module_name: Name of the neuron module to check
            :type neuron_module_name: str
            :return:
            """
            sl = SettingLoader()
            settings = sl.settings
            package_name = "kalliope.neurons" + "." + neuron_module_name.lower() + "." + neuron_module_name.lower()
            if settings.resources is not None:
                neuron_resource_path = settings.resources.neuron_folder + \
                                       os.sep + neuron_module_name.lower() + os.sep + \
                                       neuron_module_name.lower()+".py"
                if os.path.exists(neuron_resource_path):
                    imp.load_source(neuron_module_name.capitalize(), neuron_resource_path)
                    package_name = neuron_module_name.capitalize()

            try:
                mod = __import__(package_name, fromlist=[neuron_module_name.capitalize()])
                getattr(mod, neuron_module_name.capitalize())
            except AttributeError:
                raise ModuleNotFoundError("[AttributeError] The module %s does not exist in the package %s " % (neuron_module_name.capitalize(),
                                                                                                                package_name))
            except ImportError:
                raise ModuleNotFoundError("[ImportError] The module %s does not exist in the package %s " % (neuron_module_name.capitalize(),
                                                                                                             package_name))
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
        def get_key(key_name):
            try:
                return event_dict[key_name]
            except KeyError:
                return None

        if event_dict is None or event_dict == "":
            raise NoEventPeriod("Event must contain at least one of those elements: "
                                "year, month, day, week, day_of_week, hour, minute, second")

        # check content as at least on key
        year = get_key("year")
        month = get_key("month")
        day = get_key("day")
        week = get_key("week")
        day_of_week = get_key("day_of_week")
        hour = get_key("hour")
        minute = get_key("minute")
        second = get_key("second")

        list_to_check = [year, month, day, week, day_of_week, hour, minute, second]
        number_of_none_object = list_to_check.count(None)
        list_size = len(list_to_check)
        if number_of_none_object >= list_size:
            raise NoEventPeriod("Event must contain at least one of those elements: "
                                "year, month, day, week, day_of_week, hour, minute, second")

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
        .. warnings:: Static and Public
        """
        if order_dict is None or order_dict == "":
            raise NoValidOrder("An order cannot be null or empty")

        return True

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
