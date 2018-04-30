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
            raise InvalidSynapeName("Error with synapse name \"%s\"."
                                    "Valid syntax: "
                                    "At least 4 characters "
                                    "[a - zA - Z0 - 9\-] with dashes allowed in between but not at the start or end" %
                                    synape_dict["name"])

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
            if settings.resources.neuron_folder is not None:
                neuron_resource_path = settings.resources.neuron_folder + \
                                       os.sep + neuron_module_name.lower() + os.sep + \
                                       neuron_module_name.lower() + ".py"
                if os.path.exists(neuron_resource_path):
                    imp.load_source(neuron_module_name.capitalize(), neuron_resource_path)
                    package_name = neuron_module_name.capitalize()

            try:
                mod = __import__(package_name, fromlist=[neuron_module_name.capitalize()])
                getattr(mod, neuron_module_name.capitalize())
            except AttributeError:
                raise ModuleNotFoundError("[AttributeError] The module %s does not exist in the package %s " % (
                neuron_module_name.capitalize(),
                package_name))
            except ImportError:
                raise ModuleNotFoundError(
                    "[ImportError] The module %s does not exist in the package %s " % (neuron_module_name.capitalize(),
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

        def check_signal_exist(signal_name):
            """
            Return True if the signal_name python Class exist in signals package
            :param signal_name: Name of the neuron module to check
            :type signal_name: str
            :return:
            """
            sl = SettingLoader()
            settings = sl.settings
            package_name = "kalliope.signals" + "." + signal_name.lower() + "." + signal_name.lower()
            if settings.resources.signal_folder is not None:
                neuron_resource_path = settings.resources.neuron_folder + \
                                       os.sep + signal_name.lower() + os.sep + \
                                       signal_name.lower() + ".py"
                if os.path.exists(neuron_resource_path):
                    imp.load_source(signal_name.capitalize(), neuron_resource_path)
                    package_name = signal_name.capitalize()

            try:
                mod = __import__(package_name, fromlist=[signal_name.capitalize()])
                getattr(mod, signal_name.capitalize())
            except AttributeError:
                raise ModuleNotFoundError(
                    "[AttributeError] The module %s does not exist in the package %s " % (signal_name.capitalize(),
                                                                                          package_name))
            except ImportError:
                raise ModuleNotFoundError(
                    "[ImportError] The module %s does not exist in the package %s " % (signal_name.capitalize(),
                                                                                       package_name))
            return True

        if isinstance(signal_dict, dict):
            for signal_name in signal_dict:
                check_signal_exist(signal_name)
        else:
            check_signal_exist(signal_dict)
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
            seen.add(synapse_name)

        return True
