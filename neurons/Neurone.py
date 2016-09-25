import importlib
from jinja2 import Template
import random

from core import ConfigurationManager


class NoTemplateException(Exception):
    pass


class Neurone:
    def __init__(self, **kwargs):
        # get the name of the plugin
        # print self.__class__.__name__
        # load the tts from settings
        self.tts = ConfigurationManager.get_default_text_to_speech()
        # get tts args
        self.tts_args = ConfigurationManager.get_tts_args(self.tts)

    def say(self, message, kwargs):
        # get the tts if is specified otherwise use default
        tts = kwargs.get('tts', None)
        if tts is not None:
            self.tts = tts
            self.tts_args = ConfigurationManager.get_tts_args(self.tts)

        # check if it's a single message or multiple one
        if isinstance(message, list):
            # then we pick randomly one message
            message = random.choice(message)

        # Check if there is a template associate to the output message
        template = kwargs.get('say_template', None)
        if isinstance(message, dict):
            if template is not None:
                if isinstance(template, list):
                    # then we pick randomly one template
                    template = random.choice(template)
                t = Template(template)
                message = t.render(**message)
            else:
                raise NoTemplateException("You must specify a say_template to your Neurone for the entries ", message.keys())
        # here we use the tts to make jarvis talk
        # the module is imported on fly, depending on the selected tts from settings
        tts_backend = importlib.import_module("tts." + self.tts)
        tts_backend.say(words=message, **self.tts_args)