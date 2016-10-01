import logging
import os
import random

from jinja2 import Template

from core.ConfigurationManager import SettingLoader

logging.basicConfig()
logger = logging.getLogger("jarvis")


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
        logger.debug("NeuronModule called from class %s with parameters: %s" % (child_name, kwargs))

        # check if the user has overrider the TTS
        tts = kwargs.get('tts', None)
        if tts is None:
            # No tts provided,  we load the default one
            self.tts = SettingLoader().get_default_text_to_speech()
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

        if isinstance(message, str):
            logger.debug("message is string")
            tts_message = message

        if isinstance(message, list):
            logger.debug("message is list")
            tts_message = self._get_message_from_list(message)

        if isinstance(message, dict):
            logger.debug("message is dict")
            tts_message = self._get_message_from_dict(message)

        if message is not None:
            # get an instance of the target TTS
            tts_instance = self._get_tts_instance(self.tts)
            tts_args = SettingLoader().get_tts_args(self.tts)
            # change the cache settings with the one precised for the current neuron
            if self.override_cache:
                tts_args = self._update_cache_var(self.override_cache, tts_args)
            tts_instance.say(words=tts_message, **(tts_args if tts_args is not None else {}))

    @staticmethod
    def _get_message_from_list(message_list):
        """
        Return an element from the list randomly
        :param message_list:
        :return:
        """
        return random.choice(message_list)

    def _get_message_from_dict(self, message_dict):
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

        else:
            raise NoTemplateException("You must specify a say_template or a file_template")

    @staticmethod
    def _get_content_of_file(real_file_template_path):
        with open(real_file_template_path, 'r') as content_file:
            return content_file.read()

    @staticmethod
    def _get_tts_instance(tts_name):
        # capitalise for loading module name
        tts = tts_name.capitalize()
        logger.debug("Import TTS module named %s " % tts)
        mod = __import__('tts', fromlist=[str(tts)])
        try:
            klass = getattr(mod, tts)
        except ImportError, e:
            raise TTSModuleNotFound("The TTS not found: %s" % e)

        if klass is not None:
            # run the plugin
            return klass()
        else:
            raise TTSNotInstantiable("TTS module %s not instantiable" % tts)

    @staticmethod
    def _update_cache_var(new_override_cache, args_list):
        logger.debug("args for TTS plugin before update: %s" % str(args_list))
        args_list["cache"] = new_override_cache
        logger.debug("args for TTS plugin after update: %s" % str(args_list))
        return args_list
