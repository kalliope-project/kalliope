from BrainLoader import BrainLoader
from SettingLoader import SettingLoader
import logging


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
            logging.info("Default STT: %s" % default_speech_to_text)
            return default_speech_to_text
        except KeyError:
            raise DefaultSpeechToTextNotFound("Attribute default_speech_to_text not found in settings")

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

        logging.debug("Settings file content: %s" % speechs_to_text)
        # get args
        args = find(speechs_to_text, default_stt_plugin_name)

        logging.debug("Args for %s STT: %s" % (default_stt_plugin_name, args))

        return args
