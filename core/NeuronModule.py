# coding: utf8
import logging
import os
import random

import sys
from jinja2 import Template

from core import OrderListener
from core.SynapseLauncher import SynapseLauncher
from core.Utils import Utils
from core.ConfigurationManager import SettingLoader, BrainLoader

logging.basicConfig()
logger = logging.getLogger("kalliope")


class InvalidParameterException(Exception):
    pass


class MissingParameterException(Exception):
    pass


class NoTemplateException(Exception):
    pass


class MultipleTemplateException(Exception):
    pass


class TemplateFileNotFoundException(Exception):
    pass


class TTSModuleNotFound(Exception):
    pass


class TTSNotInstantiable(Exception):
    pass


class NeuronModule(object):
    def __init__(self, **kwargs):
        """
        Class used by neuron for talking
        :param kwargs: Same parameter as the Child. Can contain info about the tts to use instead of the
        default one
        """
        # get the child who called the class
        child_name = self.__class__.__name__
        logger.debug("NeuronModule called from class %s with parameters: %s" % (child_name, str(kwargs)))

        self.settings = SettingLoader.get_settings()
        self.brain = BrainLoader.get_brain()

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
        :param message: Can be a String or a dict
        :return:
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

            # create a tts object from the tts the user want to user
            tts_object = next((x for x in self.settings.ttss if x.name == self.tts), None)
            if tts_object is None:
                raise TTSModuleNotFound("The tts module name %s does not exist in settings file" % self.tts)
            # change the cache settings with the one precised for the current neuron
            if self.override_cache is not None:
                tts_object.parameter = self._update_cache_var(self.override_cache, tts_object.parameter)

            logger.debug("NeuroneModule: TTS args: %s" % tts_object)

            # get the instance of the TTS module
            tts_module_instance = Utils.get_dynamic_class_instantiation("tts", tts_object.name.capitalize(),
                                                                        tts_object.parameters)
            # generate the audio file and play it
            tts_module_instance.say(tts_message)

    def _get_message_from_dict(self, message_dict):
        """
        Generate a message taht can be played by a TTS engine from a dict of variable and the jinja template
        :param message_dict:
        :return:
        """
        returned_message = None

        if (self.say_template is not None and self.file_template is None) or \
                (self.say_template is None and self.file_template is not None):

            # the user choose a say_template option
            if self.say_template is not None:
                if isinstance(self.say_template, list):
                    # then we pick randomly one template
                    self.say_template = random.choice(self.say_template)
                t = Template(self.say_template)
                returned_message = t.render(**message_dict)

            # trick to remobe unicode problem when loading jinja template with non ascii char
            reload(sys)
            sys.setdefaultencoding('utf-8')
            # the user choose a file_template option
            if self.file_template is not None:  # the user choose a file_template option
                real_file_template_path = "templates/%s" % self.file_template
                if os.path.isfile(real_file_template_path):
                    # load the content of the file as template
                    t = Template(self._get_content_of_file(real_file_template_path))
                    returned_message = t.render(**message_dict)
                else:
                    raise TemplateFileNotFoundException("Template file %s not found in templates folder"
                                                        % real_file_template_path)
            return returned_message

        # we don't force the usage of a template. The user can choose to do nothing with returned value
        # else:
        #     raise NoTemplateException("You must specify a say_template or a file_template")

    def run_synapse_ny_name(self, name):
        SynapseLauncher.start_synapse(name=name, brain=self.brain)

    @staticmethod
    def _get_content_of_file(real_file_template_path):
        with open(real_file_template_path, 'r') as content_file:
            return content_file.read()

    @staticmethod
    def _update_cache_var(new_override_cache, args_list):
        logger.debug("args for TTS plugin before update: %s" % str(args_list))
        args_list["cache"] = new_override_cache
        logger.debug("args for TTS plugin after update: %s" % str(args_list))
        return args_list

    @staticmethod
    def get_audio_from_stt(callback):
        """
        Call the default STT to get an audio sample and return it into the callback method
        :param callback:
        :return:
        """
        # call the order listener
        oa = OrderListener(callback=callback)
        oa.start()


