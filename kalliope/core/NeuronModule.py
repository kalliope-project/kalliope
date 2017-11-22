# coding: utf8
import logging
import random
import sys

import six
from jinja2 import Template

from kalliope.core import OrderListener
from kalliope.core.HookManager import HookManager
from kalliope.core.ConfigurationManager import SettingLoader, BrainLoader
from kalliope.core.Cortex import Cortex
from kalliope.core.LIFOBuffer import LIFOBuffer
from kalliope.core.Models.MatchedSynapse import MatchedSynapse
from kalliope.core.NeuronExceptions import NeuronExceptions
from kalliope.core.OrderAnalyser import OrderAnalyser
from kalliope.core.Utils.Utils import Utils

logging.basicConfig()
logger = logging.getLogger("kalliope")


class InvalidParameterException(NeuronExceptions):
    """
    Some Neuron parameters are invalid.
    """
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super(InvalidParameterException, self).__init__(message)


class MissingParameterException(NeuronExceptions):
    """
    Some Neuron parameters are missing.
    """

    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super(MissingParameterException, self).__init__(message)


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

        sl = SettingLoader()
        self.settings = sl.settings
        brain_loader = BrainLoader()
        self.brain = brain_loader.brain

        # a dict of overridden TTS parameters if provided by the user
        self.override_tts_parameters = kwargs.get('tts', None)

        # create the TTS instance
        self.tts = None
        if self.override_tts_parameters is None or not isinstance(self.override_tts_parameters, dict):
            # we get the default TTS
            self.tts = self._get_tts_object(settings=self.settings)
        else:
            for key, value in self.override_tts_parameters.items():
                tts_name = key
                tts_parameters = value
                self.tts = self._get_tts_object(tts_name=tts_name,
                                                override_parameter=tts_parameters,
                                                settings=self.settings)

        # get templates if provided
        # Check if there is a template associate to the output message
        self.say_template = kwargs.get('say_template', None)
        # check if there is a template file associate to the output message
        self.file_template = kwargs.get('file_template', None)
        # keep the generated message
        self.tts_message = None
        # if the current call is api one
        self.is_api_call = kwargs.get('is_api_call', False)
        # if the current call want to mute kalliope
        self.no_voice = kwargs.get('no_voice', False)
        # boolean to know id the synapse is waiting for an answer
        self.is_waiting_for_answer = False
        # the synapse name to add the the buffer
        self.pending_synapse = None
        # a dict of parameters the user ask to save in short term memory
        self.kalliope_memory = kwargs.get('kalliope_memory', None)
        # parameters loaded from the order can be save now
        Cortex.save_parameter_from_order_in_memory(self.kalliope_memory)

    def __str__(self):
        retuned_string = ""
        retuned_string += self.tts_message
        return retuned_string

    def serialize(self):
        """
        This method allows to serialize in a proper way this object

        :return: A dict of name and parameters
        :rtype: Dict
        """
        self.tts_message = Utils.encode_text_utf8(self.tts_message)
        return {
            'neuron_name': self.neuron_name,
            'generated_message': self.tts_message
        }

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
        logger.debug("[NeuronModule] Say() called with message: %s" % message)

        tts_message = None

        # we can save parameters from the neuron in memory
        Cortex.save_neuron_parameter_in_memory(self.kalliope_memory, message)

        if isinstance(message, str) or isinstance(message, six.text_type):
            logger.debug("[NeuronModule] message is string")
            tts_message = message

        if isinstance(message, list):
            logger.debug("[NeuronModule] message is list")
            tts_message = random.choice(message)

        if isinstance(message, dict):
            logger.debug("[NeuronModule] message is dict")
            tts_message = self._get_message_from_dict(message)

        if tts_message is not None:
            logger.debug("[NeuronModule] tts_message to say: %s" % tts_message)
            self.tts_message = tts_message
            Utils.print_success(tts_message)

            # process the audio only if the no_voice flag is false
            if self.no_voice:
                logger.debug("[NeuronModule] no_voice is True, Kalliope is muted")
            else:
                logger.debug("[NeuronModule] no_voice is False, make Kalliope speaking")
                # get the instance of the TTS module
                tts_folder = None
                if self.settings.resources:
                    tts_folder = self.settings.resources.tts_folder
                tts_module_instance = Utils.get_dynamic_class_instantiation(package_name="tts",
                                                                            module_name=self.tts.name,
                                                                            parameters=self.tts.parameters,
                                                                            resources_dir=tts_folder)

                HookManager.on_start_speaking()
                # generate the audio file and play it
                tts_module_instance.say(tts_message)
                HookManager.on_stop_speaking()

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
        if sys.version_info[0] == 2:
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

    @staticmethod
    def run_synapse_by_name(synapse_name, user_order=None, synapse_order=None, high_priority=False,
                            is_api_call=False, overriding_parameter_dict=None, no_voice=False):
        """
        call the lifo for adding a synapse to execute in the list of synapse list to process
        :param synapse_name: The name of the synapse to run
        :param user_order: The user order
        :param synapse_order: The synapse order
        :param high_priority: If True, the synapse is executed before the end of the current synapse list
        :param is_api_call: If true, the current call comes from the api
        :param overriding_parameter_dict: dict of value to add to neuron parameters
        """
        synapse = BrainLoader().brain.get_synapse_by_name(synapse_name)
        matched_synapse = MatchedSynapse(matched_synapse=synapse,
                                         matched_order=synapse_order,
                                         user_order=user_order,
                                         overriding_parameter=overriding_parameter_dict)

        list_synapse_to_process = list()
        list_synapse_to_process.append(matched_synapse)
        # get the singleton
        lifo_buffer = LIFOBuffer()
        lifo_buffer.add_synapse_list_to_lifo(list_synapse_to_process, high_priority=high_priority)
        lifo_buffer.execute(is_api_call=is_api_call, no_voice=no_voice)

    @staticmethod
    def is_order_matching(order_said, order_match):
        return OrderAnalyser().spelt_order_match_brain_order_via_table(order_to_analyse=order_match,
                                                                       user_said=order_said)

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
    def get_audio_from_stt(callback):
        """
        Call the default STT to get an audio sample and return it into the callback method
        :param callback: A callback function
        """
        # call the order listener
        ol = OrderListener(callback=callback)
        ol.start()
        ol.join()
        # wait that the STT engine has finish his job (or the neurotransmitter neuron will be killed)
        if ol.stt_instance is not None:
            ol.stt_instance.join()

    def get_neuron_name(self):
        """
        Return the name of the neuron who call the mother class
        :return:
        """
        return self.neuron_name

    @staticmethod
    def _get_tts_object(tts_name=None, override_parameter=None, settings=None):
        """
        Return a TTS model object
        If no tts name provided, return the default TTS defined in the settings
        If the TTS name is provided, get the default configuration for this TTS in settings and override each parameters
        with parameters provided in override_parameter
        :param tts_name: name of the TTS to load
        :param override_parameter: dict of parameter to override the default configuration of the TTS
        :param settings: current settings
        :return: Tts model object
        """

        # if the tts_name is not provided, we get the default tts from settings
        if tts_name is None:
            tts_name = settings.default_tts_name

        # create a tts object from the tts the user want to use
        tts_object = next((x for x in settings.ttss if x.name == tts_name), None)
        if tts_object is None:
            raise TTSModuleNotFound("[NeuronModule] The tts module name %s does not exist in settings file" % tts_name)

        if override_parameter is not None:  # the user want to override the default TTS configuration
            logger.debug("[NeuronModule] args for TTS plugin before update: %s" % str(tts_object.parameters))
            for key, value in override_parameter.items():
                tts_object.parameters[key] = value
            logger.debug("[NeuronModule] args for TTS plugin after update: %s" % str(tts_object.parameters))

        logger.debug("[NeuronModule] TTS args: %s" % tts_object)
        return tts_object
