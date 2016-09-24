import importlib

from core import ConfigurationManager


class Neurone:
    def __init__(self, tts=None):
        # get the name of the plugin
        # print self.__class__.__name__
        # load the tts from settings
        self.tts = tts
        if tts is None:
            self.tts = ConfigurationManager.get_default_text_to_speech()
        # get tts args
        self.tts_args = ConfigurationManager.get_tts_args(self.tts)

    def say(self, message):
        # here we use the tts to make jarvis talk
        # the module is imported on fly, depending on the selected tts from settings
        tts_backend = importlib.import_module("tts." + self.tts)
        tts_backend.say(words=message, **self.tts_args)

