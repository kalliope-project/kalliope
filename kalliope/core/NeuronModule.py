# coding: utf8
import logging
import random

import sys
from jinja2 import Template

from kalliope.core import OrderListener
from kalliope.core import OrderAnalyser
from kalliope.core.SynapseLauncher import SynapseLauncher
from kalliope.core.Utils.Utils import Utils
from kalliope.core.ConfigurationManager import SettingLoader, BrainLoader

logging.basicConfig()
logger = logging.getLogger("kalliope")


class InvalidParameterException(Exception):
    """
    Some Neuron parameters are invalid.
    """
    pass


class MissingParameterException(Exception):
    """
    Some Neuron parameters are missing.
    """
    pass


class NoTemplateException(Exception):
    """
    You must specify a say_template or a file_template
    """
    pass


class TemplateFileNotFoundException(Exception):
    """
    Template file can not be found. Check the provided path.
    """
    pass


class TTSModuleNotFound(Exception):
    """
    TTS module can not be find. It must be configured in the settings file.
    """
    pass


class NeuronModule(object):
    """
    This Abstract Class is representing main Class for Neuron.
    Each Neuron must implement this Class.
    """
    def __init__(self, **kwargs):
        """
        Class used by neuron for talking
        :param kwargs: Same parameter as the Child. Can contain info about the tts to use instead of the
        default one
        """
        # get the child who called the class
        child_name = self.__class__.__name__
        self.neuron_name = child_name
        logger.debug("NeuronModule called from class %s with parameters: %s" % (child_name, str(kwargs)))

        sl = SettingLoader()
        self.settings = sl.settings
        brain_loader = BrainLoader()
        self.brain = brain_loader.brain

        # check if the user has overrider the TTS
        tts = kwargs.get('tts', None)
        if tts is None:
            # No tts provided,  we load the default one
            self.tts = self.settings.default_tts_name
        else:
            self.tts = tts

        # get if the cache settings is present
        self.override_cache = kwargs.get('cache', None)

        # get templates if provided
        # Check if there is a template associate to the output message
        self.say_template = kwargs.get('say_template', None)
        # check if there is a template file associate to the output message
        self.file_template = kwargs.get('file_template', None)

    def say(self, message):
        """
        USe TTS to speak out loud the Message.
        A message can be a string, a list or a dict
        If it's a string, simply use the TTS with the message
        If it's a list, we select randomly a string in the list and give it to the TTS
        If it's a dict, we use the template given in parameter to create a string that we give to the TTS
        :param message: Can be a String or a dict or a list

        .. raises:: TTSModuleNotFound
        """
        logger.debug("NeuronModule Say() called with message: %s" % message)

        tts_message = None

        if isinstance(message, str) or isinstance(message, unicode):
            logger.debug("message is string")
            tts_message = message

        if isinstance(message, list):
            logger.debug("message is list")
            tts_message = random.choice(message)

        if isinstance(message, dict):
            logger.debug("message is dict")
            tts_message = self._get_message_from_dict(message)

        if tts_message is not None:
            logger.debug("tts_message to say: %s" % tts_message)

            # create a tts object from the tts the user want to use
            tts_object = next((x for x in self.settings.ttss if x.name == self.tts), None)
            if tts_object is None:
                raise TTSModuleNotFound("The tts module name %s does not exist in settings file" % self.tts)
            # change the cache settings with the one precised for the current neuron
            if self.override_cache is not None:
                tts_object.parameters = self._update_cache_var(self.override_cache, tts_object.parameters)

            logger.debug("NeuroneModule: TTS args: %s" % tts_object)

            # get the instance of the TTS module
            tts_module_instance = Utils.get_dynamic_class_instantiation(package_name="tts",
                                                                        module_name=tts_object.name,
                                                                        parameters=tts_object.parameters)
            # generate the audio file and play it
            tts_module_instance.say(tts_message)

    def _get_message_from_dict(self, message_dict):
        """
        Generate a message that can be played by a TTS engine from a dict of variable and the jinja template
        :param message_dict: the dict of message
        :return: The message to say

        .. raises:: TemplateFileNotFoundException
        """
        returned_message = None

        # the user chooses a say_template option
        if self.say_template is not None:
            returned_message = self._get_say_template(self.say_template, message_dict)

        # trick to remove unicode problem when loading jinja template with non ascii char
        reload(sys)
        sys.setdefaultencoding('utf-8')

        # the user chooses a file_template option
        if self.file_template is not None:  # the user choose a file_template option
            returned_message = self._get_file_template(self.file_template, message_dict)

        return returned_message

    @staticmethod
    def _get_say_template(list_say_template, message_dict):
        if isinstance(list_say_template, list):
            # then we pick randomly one template
            list_say_template = random.choice(list_say_template)
        t = Template(list_say_template)
        return t.render(**message_dict)

    @classmethod
    def _get_file_template(cls, file_template, message_dict):
        real_file_template_path = Utils.get_real_file_path(file_template)
        if real_file_template_path is None:
            raise TemplateFileNotFoundException("Template file %s not found in templates folder"
                                                % real_file_template_path)

        # load the content of the file as template
        t = Template(cls._get_content_of_file(real_file_template_path))
        returned_message = t.render(**message_dict)

        return returned_message

    def run_synapse_by_name(self, name):
        SynapseLauncher.start_synapse(name=name, brain=self.brain)

    def is_order_matching(self, order_said, order_match):
        oa = OrderAnalyser(order=order_said, brain=self.brain)
        return oa.spelt_order_match_brain_order_via_table(order_to_analyse=order_match, user_said=order_said)

    def run_synapse_by_name_with_order(self, order, synapse_name, order_template):
        """
        Run a synapse using its name, and giving an order so it can retrieve its params.
        Useful for neurotransmitters.
        :param order: the order to match
        :param synapse_name: the name of the synapse
        :param order_template: order_template coming from the neurotransmitter
        :return: True if a synapse as been found and started using its params
        """
        synapse_to_run = self.brain.get_synapse_by_name(synapse_name=synapse_name)
        if synapse_to_run:
            # Make a list with the synapse
            logger.debug("[run_synapse_by_name_with_order]-> a synapse has been found  %s" % synapse_to_run.name)
            list_to_run = list()
            list_to_run.append(synapse_to_run)

            oa = OrderAnalyser(order=order, brain=self.brain)
            oa.start(synapses_to_run=list_to_run, external_order=order_template)
        else:
            logger.debug("[NeuronModule]-> run_synapse_by_name_with_order, the synapse has not been found : %s" % synapse_name)
        return synapse_to_run is not None

    @staticmethod
    def _get_content_of_file(real_file_template_path):
        """
        Return the content of a file in path <real_file_template_path>
        :param real_file_template_path: path of the file to return the content
        :return: file content str
        """
        with open(real_file_template_path, 'r') as content_file:
            return content_file.read()

    @staticmethod
    def _update_cache_var(new_override_cache, args_dict):
        """
        update the value for the key "cache" in the dict args_list
        :param new_override_cache: cache boolean to set in place of the current one in args_list
        :param args_dict: arg list that contain "cache" to update
        :return:
        """
        logger.debug("args for TTS plugin before update: %s" % str(args_dict))
        args_dict["cache"] = new_override_cache
        logger.debug("args for TTS plugin after update: %s" % str(args_dict))
        return args_dict

    @staticmethod
    def get_audio_from_stt(callback):
        """
        Call the default STT to get an audio sample and return it into the callback method
        :param callback: A callback function
        """
        # call the order listener
        ol = OrderListener(callback=callback)
        ol.start()
        ol.join()

    def get_neuron_name(self):
        """
        Return the name of the neuron who call the mother class
        :return:
        """
        return self.neuron_name
