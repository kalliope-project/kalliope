import logging

import jinja2
from kalliope.core.Utils.Utils import Utils

from kalliope.core.Models import Singleton
from six import with_metaclass

logging.basicConfig()
logger = logging.getLogger("kalliope")


class Cortex(with_metaclass(Singleton, object)):
    """
    short-term memories of kalliope. Used to store object with a "key" "value"
    """
    # this dict cotain the short term memory of kalliope.
    # all keys present in this dict has been saved from a user demand
    memory = dict()
    # this is a temp dict that allow us to store temporary parameters that as been loaded from the user order
    # if the user want to a key from this dict, the key and its value will be added o the memory dict
    temp = dict()

    def __init__(self):
        logger.debug("[Cortex] New memory created")

    @classmethod
    def get_memory(cls):
        """
        Get the current dict of parameters saved in memory
        :return: dict memory
        """
        return cls.memory

    @classmethod
    def save(cls, key, value):
        """
        Save a new value in the memory
        :param key: key to save
        :param value: value to save into the key
        """
        if key in cls.memory:
            logger.debug("[Cortex] key %s already present in memory with value %s. Will be overridden"
                         % (key, cls.memory[key]))
        logger.debug("[Cortex] key saved in memory. key: %s, value: %s" % (key, value))
        cls.memory[key] = value

    @classmethod
    def get_from_key(cls, key):
        try:
            return cls.memory[key]
        except KeyError:
            logger.debug("[Cortex] key %s does not exist in memory" % key)
            return None

    @classmethod
    def add_parameters_from_order(cls, dict_parameter):
        logger.debug("[Cortex] place parameters in temp list: %s" % dict_parameter)
        cls.temp.update(dict_parameter)

    @classmethod
    def get_parameters_from_order(cls):
        """
        return the current list of
        :return:
        """
        return cls.temp

    @classmethod
    def clean_parameter_from_order(cls):
        """
        Clean the temps memory that store parameters loaded from vocal order
        """
        logger.debug("[Cortex] Clean temp memory")
        cls.temp = dict()

    @classmethod
    def save_memory(cls, dict_parameter_to_save, neuron_parameters):
        """
        receive a dict of value send by the child neuron
        save in kalliope memory all value

        E.g
        dict_parameter_to_save = {"my_key_to_save_in_memory": "{{ output_val_from_neuron }}"}
        neuron_parameter = {"output_val_from_neuron": "this_is_a_value" }

        then the cortex will save in memory the key "my_key_to_save_in_memory" and attach the value "this_is_a_value"

        :param neuron_parameters: dict of parameter the neuron has processed and send to the neurone module to
                be processed by the TTS engine
        :param dict_parameter_to_save: a dict of key value the user want to save from the dict_neuron_parameter
        """

        if dict_parameter_to_save is not None:
            logger.debug("[NeuronModule] save_memory - User want to save: %s" % dict_parameter_to_save)
            logger.debug("[NeuronModule] save_memory - Available parameters in the neuron: %s" % neuron_parameters)
            logger.debug("[NeuronModule] save_memory - Available parameters in orders: %s"
                         % Cortex.get_parameters_from_order())

            for dict_key_val in dict_parameter_to_save:
                for key, value in dict_key_val.items():
                    # ask the cortex to save in memory the target "key" if it was in parameters of the neuron
                    if isinstance(neuron_parameters, dict):
                        if Utils.is_containing_bracket(value):
                            value = jinja2.Template(value).render(neuron_parameters)
                        Cortex.save(key, value)

                    # ask the cortex to save in memory the target "key" if it was in the order
                    if Utils.is_containing_bracket(value):
                        value = jinja2.Template(value).render(Cortex.get_parameters_from_order())
                        Cortex.save(key, value)
