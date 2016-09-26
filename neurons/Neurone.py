import importlib

from core import ConfigurationManager


class TTSModuleNotFound(Exception):
    pass


class TTSNotInstantiable(Exception):
    pass


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
        self.tts = self.tts.capitalize()
        print "tts args: %s" % str(self.tts_args)

        # instantiate the TTS
        self.tts_instance = self._get_tts_instance()

    def say(self, message):
        # here we use the tts to make jarvis talk
        # the module is imported on fly, depending on the selected tts from settings
        self.tts_instance.say(words=message, **(self.tts_args if self.tts_args is not None else {}))

    def _get_tts_instance(self):
        print "Import TTS module named %s " % self.tts
        mod = __import__('tts', fromlist=[self.tts])
        try:
            klass = getattr(mod, self.tts)
        except ImportError, e:
            raise TTSModuleNotFound("The TTS not found: %s" % e)

        if klass is not None:
            # run the plugin
            return klass()
        else:
            raise TTSNotInstantiable("TTS module %s not instantiable" % self.tts)
