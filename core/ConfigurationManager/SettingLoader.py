import logging

from YAMLLoader import YAMLLoader
from core.FileManager import FileManager
from core.Models import Singleton
from core.Models.RestAPI import RestAPI
from core.Models.Settings import Settings
from core.Models.Stt import Stt
from core.Models.Trigger import Trigger
from core.Models.Tts import Tts

FILE_NAME = "settings.yml"

logging.basicConfig()
logger = logging.getLogger("kalliope")


class SettingInvalidException(Exception):
    pass


class NullSettingException(Exception):
    pass


class SettingNotFound(Exception):
    pass

@Singleton
class SettingLoader(object):

    def __init__(self):
        # Todo check how to provide the file_path
        self.settings = self._get_settings()
        self.yaml_config = self._get_yaml_config()

    @classmethod
    def _get_yaml_config(cls, file_path=None):
        if file_path is None:
            file_path = FILE_NAME
        return YAMLLoader.get_config(file_path)

    @classmethod
    def _get_settings(cls, file_path=None):
        """
        Return a Settings object from settings.yml file
        :return:
        """
        settings = cls.get_yaml_config(file_path)
        default_stt_name = cls._get_default_speech_to_text(settings)
        default_tts_name = cls._get_default_text_to_speech(settings)
        default_trigger_name = cls._get_default_trigger(settings)
        stts = cls._get_stts(settings)
        ttss = cls._get_ttss(settings)
        triggers = cls._get_triggers(settings)
        random_wake_up_answers = cls._get_random_wake_up_answers(settings)
        random_wake_up_sounds = cls._get_random_wake_up_sounds(settings)
        rest_api = cls._get_rest_api(settings)
        cache_path = cls._get_cache_path(settings)

        # create a setting object
        setting_object = Settings(default_stt_name=default_stt_name,
                                  default_tts_name=default_tts_name,
                                  default_trigger_name=default_trigger_name,
                                  stts=stts,
                                  ttss=ttss,
                                  triggers=triggers,
                                  random_wake_up_answers=random_wake_up_answers,
                                  random_wake_up_sounds=random_wake_up_sounds,
                                  rest_api=rest_api,
                                  cache_path=cache_path)
        return setting_object

    @staticmethod
    def _get_default_speech_to_text(settings):

        try:
            default_speech_to_text = settings["default_speech_to_text"]
            if default_speech_to_text is None:
                raise NullSettingException("Attribute default_speech_to_text is null")
            logger.debug("Default STT: %s" % default_speech_to_text)
            return default_speech_to_text
        except KeyError, e:
            raise SettingNotFound("%s setting not found" % e)

    @staticmethod
    def _get_default_text_to_speech(settings):
        try:
            default_text_to_speech = settings["default_text_to_speech"]
            if default_text_to_speech is None:
                raise NullSettingException("Attribute default_text_to_speech is null")
            logger.debug("Default TTS: %s" % default_text_to_speech)
            return default_text_to_speech
        except KeyError, e:
            raise SettingNotFound("%s setting not found" % e)

    @staticmethod
    def _get_default_trigger(settings):
        try:
            default_trigger = settings["default_trigger"]
            if default_trigger is None:
                raise NullSettingException("Attribute default_trigger is null")
            logger.debug("Default Trigger name: %s" % default_trigger)
            return default_trigger
        except KeyError, e:
            raise SettingNotFound("%s setting not found" % e)

    @classmethod
    def _get_stts(cls, settings):
        """
        Return a list of stt object
        :param settings: loaded settings file
        :return: List of Stt
        """
        try:
            speechs_to_text_list = settings["speech_to_text"]
        except KeyError:
            raise NullSettingException("speech_to_text settings not found")

        stts = list()
        for speechs_to_text_el in speechs_to_text_list:
            if isinstance(speechs_to_text_el, dict):
                # print "Neurons dict ok"
                for stt_name in speechs_to_text_el:
                    name = stt_name
                    parameters = speechs_to_text_el[name]
                    new_stt = Stt(name=name, parameters=parameters)
                    stts.append(new_stt)
            else:
                # the neuron does not have parameter
                new_stt = Stt(name=speechs_to_text_el)
                stts.append(new_stt)
        return stts

    @classmethod
    def _get_ttss(cls, settings):
        """
        Return a list of Tts object
        :param settings: loaded settings file
        :return: List of Tts
        """
        try:
            text_to_speech_list = settings["text_to_speech"]
        except KeyError, e:
            raise SettingNotFound("%s setting not found" % e)

        ttss = list()
        for text_to_speech_el in text_to_speech_list:
            if isinstance(text_to_speech_el, dict):
                # print "Neurons dict ok"
                for tts_name in text_to_speech_el:
                    name = tts_name
                    parameters = text_to_speech_el[name]
                    new_tts = Tts(name=name, parameters=parameters)
                    ttss.append(new_tts)
            else:
                # the neuron does not have parameter
                new_tts = Tts(name=text_to_speech_el)
                ttss.append(new_tts)
        return ttss

    @classmethod
    def _get_triggers(cls, settings):
        """
        Return a list of Trigger object
        :param settings: loaded settings file
        :return: List of Trigger
        """
        try:
            triggers_list = settings["triggers"]
        except KeyError, e:
            raise SettingNotFound("%s setting not found" % e)

        triggers = list()
        for trigger_el in triggers_list:
            if isinstance(trigger_el, dict):
                # print "Neurons dict ok"
                for tts_name in trigger_el:
                    name = tts_name
                    parameters = trigger_el[name]
                    new_tts = Trigger(name=name, parameters=parameters)
                    triggers.append(new_tts)
            else:
                # the neuron does not have parameter
                new_tts = Trigger(name=trigger_el)
                triggers.append(new_tts)
        return triggers

    @classmethod
    def _get_random_wake_up_answers(cls, settings):
        """
        return a list of string
        :param settings:
        :return:
        """
        try:
            random_wake_up_answers_list = settings["random_wake_up_answers"]
        except KeyError:
            # User does not provide this settings
            return None

        # The list cannot be empty
        if random_wake_up_answers_list is None:
            raise NullSettingException("random_wake_up_answers settings is null")

        return random_wake_up_answers_list

    @classmethod
    def _get_random_wake_up_sounds(cls, settings):
        """
        return a list of string
        :param settings:
        :return: List of string
        """
        try:
            random_wake_up_sounds_list = settings["random_wake_up_sounds"]
        except KeyError:
            # User does not provide this settings
            return None

        # The the setting is present, the list cannot be empty
        if random_wake_up_sounds_list is None:
            raise NullSettingException("random_wake_up_sounds settings is empty")

        return random_wake_up_sounds_list

    @classmethod
    def _get_rest_api(cls, settings):
        try:
            rest_api = settings["rest_api"]
        except KeyError, e:
            raise SettingNotFound("%s setting not found" % e)

        if rest_api is not None:
            try:
                password_protected = rest_api["password_protected"]
                if password_protected is None:
                    raise NullSettingException("password_protected setting cannot be null")
                login = rest_api["login"]
                password = rest_api["password"]
                if password_protected:
                    if login is None:
                        raise NullSettingException("login setting cannot be null if password_protected is True")
                    if login is None:
                        raise NullSettingException("password setting cannot be null if password_protected is True")
                active = rest_api["active"]
                if active is None:
                    raise NullSettingException("active setting cannot be null")
                port = rest_api["port"]
                if port is None:
                    raise NullSettingException("port setting cannot be null")
                # check that the port in an integer
                try:
                    port = int(port)
                except ValueError:
                    raise SettingInvalidException("port must be an integer")
                # check the port is a valid port number
                if not 1024 <= port <= 65535:
                    raise SettingInvalidException("port must be in range 1024-65535")

            except KeyError, e:
                # print e
                raise SettingNotFound("%s settings not found" % e)

            # config ok, we can return the rest api object
            rest_api_obj = RestAPI(password_protected=password_protected, login=login, password=password, active=active, port=port)
            return rest_api_obj
        else:
            raise NullSettingException("rest_api settings cannot be null")

    @classmethod
    def _get_cache_path(cls, settings):
        try:
            cache_path = settings["cache_path"]
        except KeyError, e:
            raise SettingNotFound("%s setting not found" % e)

        if cache_path is None:
            raise NullSettingException("cache_path setting cannot be null")

        # test if that path is usable
        if FileManager.is_path_exists_or_creatable(cache_path):
            return cache_path
        else:
            raise SettingInvalidException("The cache_path seems to be invalid: %s" % cache_path)
