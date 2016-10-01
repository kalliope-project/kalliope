from BrainLoader import BrainLoader
from SettingLoader import SettingLoader
import logging

logging.basicConfig()
logger = logging.getLogger("jarvis")


class DefaultSpeechToTextNotFound(Exception):
    pass


class DefaultSpeechNull(Exception):
    pass


class NoSpeechToTextConfiguration(Exception):
    pass


class ConfigurationManager:

    def __init__(self):
        pass

    @classmethod
    def get_brain(cls, brain_file_name=None):
        if brain_file_name is None:
            brain_file_name = "brain.yml"
        return BrainLoader(brain_file_name).get_config()

    @classmethod
    def get_settings(cls, setting_file_name=None):
        if setting_file_name is None:
            setting_file_name = "settings.yml"
        return SettingLoader(setting_file_name).get_config()

    @classmethod
    def get_default_speech_to_text(cls):
        settings = cls.get_settings()

        try:
            default_speech_to_text = settings["default_speech_to_text"]
            if default_speech_to_text is None:
                raise DefaultSpeechNull("Attribute default_speech_to_text is null")
            logger.debug("Default STT: %s" % default_speech_to_text)
            return default_speech_to_text
        except KeyError:
            raise DefaultSpeechToTextNotFound("Attribute default_speech_to_text not found in settings")

    @classmethod
    def get_default_text_to_speech(cls):
        settings = cls.get_settings()

        try:
            default_text_to_speech = settings["default_text_to_speech"]
            if default_text_to_speech is None:
                raise DefaultSpeechNull("Attribute default_text_to_speech is null")
            logger.debug("Default TTS: %s" % default_text_to_speech)
            return default_text_to_speech
        except KeyError:
            raise DefaultSpeechToTextNotFound("Attribute default_text_to_speech not found in settings")

    @classmethod
    def get_stt_args(cls, default_stt_plugin_name):
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

        settings = cls.get_settings()
        try:
            speechs_to_text = settings["speech_to_text"]
        except KeyError:
            raise NoSpeechToTextConfiguration("No speech_to_text in settings")

        logger.debug("Settings file content: %s" % speechs_to_text)
        # get args
        args = find(speechs_to_text, default_stt_plugin_name)

        logger.debug("Args for %s STT: %s" % (default_stt_plugin_name, args))

        return args

    @classmethod
    def get_tts_args(cls, tts_name):
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

        settings = cls.get_settings()
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

    @classmethod
    def get_tts_list(cls):
        settings = cls.get_settings()
        try:
            texts_to_speech = settings["text_to_speech"]
        except KeyError:
            raise NoSpeechToTextConfiguration("No text_to_speech in settings")

        return texts_to_speech

    @classmethod
    def get_stt_list(cls):
        settings = cls.get_settings()
        try:
            speech_to_text = settings["speech_to_text"]
        except KeyError:
            raise NoSpeechToTextConfiguration("No speech_to_text in settings")

        return speech_to_text
