from YAMLLoader import YAMLLoader
import logging

FILE_NAME = "settings.yml"

logging.basicConfig()
logger = logging.getLogger("jarvis")


class DefaultSpeechToTextNotFound(Exception):
    pass


class DefaultSpeechNull(Exception):
    pass


class NoSpeechToTextConfiguration(Exception):
    pass


class SettingLoader(YAMLLoader):

    def __init__(self, filename=None):
        self.fileName = filename
        if filename is None:
            self.fileName = FILE_NAME
        self.filePath = "../../" + self.fileName
        YAMLLoader.__init__(self, self.filePath)

    def get_config(self):
        return YAMLLoader.get_config(self)

    def get_default_speech_to_text(self):
        settings = self.get_config()

        try:
            default_speech_to_text = settings["default_speech_to_text"]
            if default_speech_to_text is None:
                raise DefaultSpeechNull("Attribute default_speech_to_text is null")
            logger.debug("Default STT: %s" % default_speech_to_text)
            return default_speech_to_text
        except KeyError:
            raise DefaultSpeechToTextNotFound("Attribute default_speech_to_text not found in settings")

    def get_default_text_to_speech(self):
        settings = self.get_config()

        try:
            default_text_to_speech = settings["default_text_to_speech"]
            if default_text_to_speech is None:
                raise DefaultSpeechNull("Attribute default_text_to_speech is null")
            logger.debug("Default TTS: %s" % default_text_to_speech)
            return default_text_to_speech
        except KeyError:
            raise DefaultSpeechToTextNotFound("Attribute default_text_to_speech not found in settings")

    def get_stt_args(self, default_stt_plugin_name):
        """
        Return argument set for the current STT engine
        :param default_stt_plugin_name: Name of the STT engine
        :return:
        """

        def find(lst, key):
            """
            Find a key name in a list
            :param lst: list()
            :param key: key name to find i the list
            :return: Return the dict
            """
            for el in lst:
                try:
                    if el[key]:
                        return el[key]
                except TypeError:
                    pass
                except KeyError:
                    pass
            return None

        settings = self.get_config()
        try:
            speechs_to_text = settings["speech_to_text"]
        except KeyError:
            raise NoSpeechToTextConfiguration("No speech_to_text in settings")

        logger.debug("Settings file content: %s" % speechs_to_text)
        # get args
        args = find(speechs_to_text, default_stt_plugin_name)

        logger.debug("Args for %s STT: %s" % (default_stt_plugin_name, args))

        return args

    def get_tts_args(self, tts_name):
        """
        Return argument set for the current STT engine
        :param tts_name: Name of the TTS engine
        :return:
        """

        def find(lst, key):
            """
            Find a key name in a list
            :param lst: list()
            :param key: key name to find i the list
            :return: Return the dict
            """
            for el in lst:
                try:
                    if el[key]:
                        return el[key]
                except TypeError:
                    pass
                except KeyError:
                    pass
            return None

        settings = self.get_config()
        try:
            texts_to_speech = settings["text_to_speech"]
        except KeyError:
            raise NoSpeechToTextConfiguration("No text_to_speech in settings")

        logger.debug("Settings file content: %s" % texts_to_speech)
        # get args
        args = find(texts_to_speech, tts_name)
        logger.debug("Args for %s TTS: %s" % (tts_name, args))
        # print args
        return args
