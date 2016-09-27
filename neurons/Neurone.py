import importlib
from jinja2 import Template
import random
import os.path
import logging

from core import ConfigurationManager


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


class Neurone:
    def __init__(self, **kwargs):
        # get the name of the plugin who load Neurone mother class
        # print self.__class__.__name__

        print "Neurone class called with parameters: %s" % kwargs

        # get the tts if is specified otherwise use default
        tts = kwargs.get('tts', None)
        if tts is not None:
            self.tts = tts
        else:
            self.tts = ConfigurationManager.get_default_text_to_speech()
        # get tts args
        self.tts_args = ConfigurationManager.get_tts_args(self.tts)
        # capitalise for loading module name
        self.tts = self.tts.capitalize()
        # load the module
        self.tts_instance = self._get_tts_instance()

    def say(self, message, kwargs):
        # get the tts if is specified otherwise use default
        tts = kwargs.get('tts', None)
        if tts is not None:
            self.tts = tts
            self.tts_args = ConfigurationManager.get_tts_args(self.tts)

        # get if the cache settings is present
        override_cache = kwargs.get('cache', None)
        if override_cache is not None:
            # the user set the "cache var"
            self.tts_args = self._update_cache_var(override_cache)

        # check if it's a single message or multiple one
        if isinstance(message, list):
            # then we pick randomly one message
            message = random.choice(message)

        # Check if there is a template associate to the output message
        say_template = kwargs.get('say_template', None)
        # check if there is a template file associate to the output message
        file_template = kwargs.get('file_template', None)

        # we check if the user provide a say_template or a file_template, Not both
        if say_template is not None and file_template is not None:
            raise MultipleTemplateException("You must provide a say_template or a file_template, not both")

        # check on of the two option is set
        if isinstance(message, dict):
            if (say_template is not None and file_template is None) or \
                    (say_template is None and file_template is not None):
                if say_template is not None:    # the user choose a say_template option
                    if isinstance(say_template, list):
                        # then we pick randomly one template
                        say_template = random.choice(say_template)
                    t = Template(say_template)
                    message = t.render(**message)
                if file_template is not None:   # the user choose a file_template option
                    real_file_template_path = "templates/%s" % file_template
                    if os.path.isfile(real_file_template_path):
                        # load the content of the file as template
                        t = Template(self._get_content_of_file(real_file_template_path))
                        message = t.render(**message)
                    else:
                        raise TemplateFileNotFoundException("Template file %s not found in templates folder"
                                                            % real_file_template_path)

            else:
                raise NoTemplateException("You must specify a say_template or a file_template", message.keys())

        # here we use the tts to make jarvis talk
        # the module is imported on fly, depending on the selected tts from settings
        self.tts_instance.say(words=message, **(self.tts_args if self.tts_args is not None else {}))

    def _get_tts_instance(self):
        logging.info("Import TTS module named %s " % self.tts)
        mod = __import__('tts', fromlist=[str(self.tts)])
        try:
            klass = getattr(mod, self.tts)
        except ImportError, e:
            raise TTSModuleNotFound("The TTS not found: %s" % e)

        if klass is not None:
            # run the plugin
            return klass()
        else:
            raise TTSNotInstantiable("TTS module %s not instantiable" % self.tts)

    @staticmethod
    def _check_file_exist(real_file_template):
        return os.path.isfile(real_file_template)

    @staticmethod
    def _get_content_of_file(real_file_template_path):
        with open(real_file_template_path, 'r') as content_file:
            return content_file.read()

    def _update_cache_var(self, override_cache):
        print "args for TTS plugin before update: %s" % str(self.tts_args)
        self.tts_args["cache"] = override_cache

        print "args for TTS plugin after update: %s" % str(self.tts_args)
        return self.tts_args
