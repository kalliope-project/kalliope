import logging

import jinja2
import six

from kalliope.core.ConfigurationManager.SettingLoader import SettingLoader
from kalliope.core.Cortex import Cortex
from kalliope.core.NeuronExceptions import NeuronExceptions
from kalliope.core.Utils.Utils import Utils

logging.basicConfig()
logger = logging.getLogger("kalliope")


class NeuronParameterNotAvailable(Exception):
    pass


class NeuronLauncher:

    def __init__(self):
        pass

    @classmethod
    def launch_neuron(cls, neuron):
        """
        Start a neuron plugin
        :param neuron: neuron object
        :type neuron: Neuron
        :return:
        """
        logger.debug("Run neuron: \"%s\"" % (neuron.__str__()))
        settings = cls.load_settings()
        neuron_folder = None
        if settings.resources:
            neuron_folder = settings.resources.neuron_folder

        return Utils.get_dynamic_class_instantiation(package_name="neurons",
                                                     module_name=neuron.name,
                                                     parameters=neuron.parameters,
                                                     resources_dir=neuron_folder)

    @classmethod
    def start_neuron(cls, neuron, parameters_dict=None):
        """
        Execute each neuron from the received neuron_list.
        Replace parameter if exist in the received dict of parameters_dict
        :param neuron: Neuron object to run
        :param parameters_dict: dict of parameter to load in each neuron if expecting a parameter
        :return: List of the instantiated neurons (no errors detected)
        """
        if neuron.parameters is not None:
            try:
                neuron.parameters = cls._replace_brackets_by_loaded_parameter(neuron.parameters, parameters_dict)
            except NeuronParameterNotAvailable:
                Utils.print_danger("Missing parameter in neuron %s. Execution skipped" % neuron.name)
                return None
        try:
            instantiated_neuron = NeuronLauncher.launch_neuron(neuron)
        except NeuronExceptions as e:
            Utils.print_danger("ERROR: Fail to execute neuron '%s'. "
                               '%s' ". -> Execution skipped" % (neuron.name, e.message))
            return None
        return instantiated_neuron

    @classmethod
    def _replace_brackets_by_loaded_parameter(cls, neuron_parameters, loaded_parameters):
        """
        Receive a value (which can be a str or dict or list) and instantiate value in double brace bracket
        by the value specified in the loaded_parameters dict.
        This method will call itself until all values has been instantiated
        :param neuron_parameters: value to instantiate. Str or dict or list
        :param loaded_parameters: dict of parameters
        """
        logger.debug("[NeuronLauncher] replacing brackets from %s, using %s" % (neuron_parameters, loaded_parameters))
        # add variables from the short term memory to the list of loaded parameters that can be used in a template
        # the final dict is added into a key "kalliope_memory" to not override existing keys loaded form the order
        memory_dict = dict()
        memory_dict["kalliope_memory"] = Cortex.get_memory()
        if loaded_parameters is None:
            loaded_parameters = dict()  # instantiate an empty dict in order to be able to add memory in it
        loaded_parameters.update(memory_dict)
        if isinstance(neuron_parameters, str) or isinstance(neuron_parameters, six.text_type):
            # replace bracket parameter only if the str contains brackets
            if Utils.is_containing_bracket(neuron_parameters):
                # check that the parameter to replace is available in the loaded_parameters dict
                if cls._neuron_parameters_are_available_in_loaded_parameters(neuron_parameters, loaded_parameters):
                    # add parameters from global variable into the final loaded parameter dict
                    settings = cls.load_settings()
                    loaded_parameters.update(settings.variables)
                    neuron_parameters = jinja2.Template(neuron_parameters).render(loaded_parameters)
                    neuron_parameters = Utils.encode_text_utf8(neuron_parameters)
                    return str(neuron_parameters)
                else:
                    raise NeuronParameterNotAvailable
            return neuron_parameters

        if isinstance(neuron_parameters, dict):
            returned_dict = dict()
            for key, value in neuron_parameters.items():
                # following keys are reserved by kalliope core
                if key in "say_template" or key in "file_template" or key in "kalliope_memory" \
                        or key in "from_answer_link":
                    returned_dict[key] = value
                else:
                    returned_dict[key] = cls._replace_brackets_by_loaded_parameter(value, loaded_parameters)
            return returned_dict

        if isinstance(neuron_parameters, list):
            returned_list = list()
            for el in neuron_parameters:
                templated_value = cls._replace_brackets_by_loaded_parameter(el, loaded_parameters)
                returned_list.append(templated_value)
            return returned_list
        # in all other case (boolean or int for example) we return the value as it
        return neuron_parameters

    @staticmethod
    def _neuron_parameters_are_available_in_loaded_parameters(string_parameters, loaded_parameters):
        """
        Check that all parameters in brackets are available in the loaded_parameters dict
        
        E.g:
        string_parameters = "this is a {{ parameter1 }}"
        
        Will return true if the loaded_parameters looks like the following
        loaded_parameters { "parameter1": "a value"}        
        
        :param string_parameters: The string that contains one or more parameters in brace brackets
        :param loaded_parameters: Dict of parameter
        :return: True if all parameters in brackets have an existing key in loaded_parameters dict
        """
        list_parameters_with_brackets = Utils.find_all_matching_brackets(string_parameters)
        # remove brackets to keep only the parameter name
        for parameter_with_brackets in list_parameters_with_brackets:
            parameter = Utils.remove_spaces_in_brackets(parameter_with_brackets)
            parameter = parameter.replace("{{", "").replace("}}", "")
            if loaded_parameters is None or parameter not in loaded_parameters:
                Utils.print_danger("The parameter %s is not available in the order" % str(parameter))
                return False
        return True

    @staticmethod
    def load_settings():
        """
        Return loaded kalliope settings
        :return: setting object
        """
        sl = SettingLoader()
        return sl.settings
