import logging

from kalliope.core.Utils.Utils import Utils
from kalliope.core.ConfigurationManager.SettingLoader import SettingLoader

logging.basicConfig()
logger = logging.getLogger("kalliope")


class NeuronLauncher:

    def __init__(self):
        pass

    @classmethod
    def start_neuron(cls, neuron):
        """
        Start a neuron plugin
        :param neuron: neuron object
        :type neuron: Neuron
        :return:
        """
        logger.debug("Run plugin \"%s\" with parameters %s" % (neuron.name, neuron.parameters))
        sl = SettingLoader()
        settings = sl.settings
        neuron_folder = None
        if settings.resources:
            neuron_folder = settings.resources.neuron_folder

        cls._replace_global_variables(neuron, settings)

        return Utils.get_dynamic_class_instantiation(package_name="neurons",
                                                     module_name=neuron.name,
                                                     parameters=neuron.parameters,
                                                     resources_dir=neuron_folder)

    @classmethod
    def _replace_global_variables(cls, neuron, settings):
        """
        Replace all the parameters with variables with the variable value.
        :param neuron: the neuron
        :param settings: the settings
        """
        for param in neuron.parameters:
            if isinstance(neuron.parameters[param], list):
                list_param_value = list()
                for sentence in neuron.parameters[param]:
                    sentence_with_global_variables = cls._get_global_variable(sentence=sentence,
                                                                              settings=settings)
                    list_param_value.append(sentence_with_global_variables)
                neuron.parameters[param] = list_param_value

            else:
                if Utils.is_containing_bracket(neuron.parameters[param]):
                    sentence_with_global_variables = cls._get_global_variable(sentence=neuron.parameters[param],
                                                                              settings=settings)
                    neuron.parameters[param] = sentence_with_global_variables

    @staticmethod
    def _get_global_variable(sentence, settings):
        """
        Get the global variable from the sentence with brackets
        :param sentence: the sentence to check
        :return: the global variable
        """
        sentence_no_spaces = Utils.remove_spaces_in_brackets(sentence=sentence)
        list_of_bracket_params = Utils.find_all_matching_brackets(sentence=sentence_no_spaces)
        for param_with_bracket in list_of_bracket_params:
            param_no_brackets = param_with_bracket.replace("{{", "").replace("}}", "")
            if param_no_brackets in settings.variables:
                logger.debug("Replacing variable %s with  %s" % (param_with_bracket,
                                                                 settings.variables[param_no_brackets]))
                sentence_no_spaces = sentence_no_spaces.replace(param_with_bracket,
                                                                str(settings.variables[param_no_brackets]))
        return sentence_no_spaces
