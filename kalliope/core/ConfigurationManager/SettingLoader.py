import logging
import os

from YAMLLoader import YAMLLoader
from kalliope.core.Models.Resources import Resources
from kalliope.core.Utils.Utils import Utils
from kalliope.core.Models import Singleton
from kalliope.core.Models.RestAPI import RestAPI
from kalliope.core.Models.Settings import Settings
from kalliope.core.Models.Stt import Stt
from kalliope.core.Models.Trigger import Trigger
from kalliope.core.Models.Tts import Tts
from kalliope.core.Utils.FileManager import FileManager

FILE_NAME = "settings.yml"

logging.basicConfig()
logger = logging.getLogger("kalliope")


class SettingInvalidException(Exception):
    """
    Some data must match the expected value/type

    .. seealso:: Settings
    """
    pass


class NullSettingException(Exception):
    """
    Some Attributes can not be Null

    .. seealso:: Settings
    """
    pass


class SettingNotFound(Exception):
    """
    Some Attributes are missing

    .. seealso:: Settings
    """
    pass


class SettingLoader(object):
    """
    This Class is used to get the Settings YAML and the Settings as an object
    """
    __metaclass__ = Singleton

    def __init__(self, file_path=None):
        self.file_path = file_path
        if self.file_path is None:
            self.file_path = Utils.get_real_file_path(FILE_NAME)
        else:
            self.file_path = Utils.get_real_file_path(file_path)
        # if the returned file path is none, the file doesn't exist
        if self.file_path is None:
            raise SettingNotFound("Settings.yml file not found")
        self.yaml_config = self._get_yaml_config()
        self.settings = self._get_settings()

    def _get_yaml_config(self):
        """
        Class Methods which loads default or the provided YAML file and return it as a String

        :return: The loaded settings YAML
        :rtype: dict

        :Example:
            settings_yaml = SettingLoader.get_yaml_config(/var/tmp/settings.yml)

        .. warnings:: Class Method
        """
        return YAMLLoader.get_config(self.file_path)

    def _get_settings(self):
        """
        Class Methods which loads default or the provided YAML file and return a Settings Object

        :return: The loaded Settings
        :rtype: Settings

        :Example:

            settings = SettingLoader.get_settings(file_path="/var/tmp/settings.yml")

        .. seealso:: Settings
        .. warnings:: Class Method
        """

        # create a new setting
        setting_object = Settings()

        # Get the setting parameters
        settings = self._get_yaml_config()
        default_stt_name = self._get_default_speech_to_text(settings)
        default_tts_name = self._get_default_text_to_speech(settings)
        default_trigger_name = self._get_default_trigger(settings)
        stts = self._get_stts(settings)
        ttss = self._get_ttss(settings)
        triggers = self._get_triggers(settings)
        random_wake_up_answers = self._get_random_wake_up_answers(settings)
        random_wake_up_sounds = self._get_random_wake_up_sounds(settings)
        rest_api = self._get_rest_api(settings)
        cache_path = self._get_cache_path(settings)
        default_synapse = self._get_default_synapse(settings)
        resources = self._get_resources(settings)

        # Load the setting singleton with the parameters
        setting_object.default_tts_name = default_tts_name
        setting_object.default_stt_name = default_stt_name
        setting_object.default_trigger_name = default_trigger_name
        setting_object.stts = stts
        setting_object.ttss = ttss
        setting_object.triggers = triggers
        setting_object.random_wake_up_answers = random_wake_up_answers
        setting_object.random_wake_up_sounds = random_wake_up_sounds
        setting_object.rest_api = rest_api
        setting_object.cache_path = cache_path
        setting_object.default_synapse = default_synapse
        setting_object.resources = resources

        return setting_object

    @staticmethod
    def _get_default_speech_to_text(settings):
        """
        Get the default speech to text defined in the settings.yml file

        :param settings: The YAML settings file
        :type settings: dict
        :return: the default speech to text
        :rtype: str

        :Example:

            default_stt_name = cls._get_default_speech_to_text(settings)

        .. seealso:: Stt
        .. raises:: NullSettingException, SettingNotFound
        .. warnings:: Static and Private
        """

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
        """
        Get the default text to speech defined in the settings.yml file

        :param settings: The YAML settings file
        :type settings: dict
        :return: the default text to speech
        :rtype: str

        :Example:

            default_tts_name = cls._get_default_text_to_speech(settings)

        .. seealso:: Tts
        .. raises:: NullSettingException, SettingNotFound
        .. warnings:: Static and Private
        """

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
        """
        Get the default trigger defined in the settings.yml file
        :param settings: The YAML settings file
        :type settings: dict
        :return: the default trigger
        :rtype: str

        :Example:

            default_trigger_name = cls._get_default_trigger(settings)

        .. seealso:: Trigger
        .. raises:: NullSettingException, SettingNotFound
        .. warnings:: Static and Private
        """

        try:
            default_trigger = settings["default_trigger"]
            if default_trigger is None:
                raise NullSettingException("Attribute default_trigger is null")
            logger.debug("Default Trigger name: %s" % default_trigger)
            return default_trigger
        except KeyError, e:
            raise SettingNotFound("%s setting not found" % e)

    @staticmethod
    def _get_stts(settings):
        """
        Return a list of stt object

        :param settings: The YAML settings file
        :type settings: dict
        :return: List of Stt
        :rtype: list

        :Example:

            stts = cls._get_stts(settings)

        .. seealso:: Stt
        .. raises:: SettingNotFound
        .. warnings:: Class Method and Private
        """

        try:
            speechs_to_text_list = settings["speech_to_text"]
        except KeyError:
            raise SettingNotFound("speech_to_text settings not found")

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

    @staticmethod
    def _get_ttss(settings):
        """

        Return a list of stt object

        :param settings: The YAML settings file
        :type settings: dict
        :return: List of Ttss
        :rtype: list

        :Example:

            ttss = cls._get_ttss(settings)

        .. seealso:: Tts
        .. raises:: SettingNotFound
        .. warnings:: Class Method and Private
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

    @staticmethod
    def _get_triggers(settings):
        """
        Return a list of Trigger object

        :param settings: The YAML settings file
        :type settings: dict
        :return: List of Trigger
        :rtype: list

        :Example:

            triggers = cls._get_triggers(settings)

        .. seealso:: Trigger
        .. raises:: SettingNotFound
        .. warnings:: Class Method and Private
        """

        try:
            triggers_list = settings["triggers"]
        except KeyError, e:
            raise SettingNotFound("%s setting not found" % e)

        triggers = list()
        for trigger_el in triggers_list:
            if isinstance(trigger_el, dict):
                # print "Neurons dict ok"
                for trigger_name in trigger_el:
                    name = trigger_name
                    parameters = trigger_el[name]
                    new_trigger = Trigger(name=name, parameters=parameters)
                    triggers.append(new_trigger)
            else:
                # the neuron does not have parameter
                new_trigger = Trigger(name=trigger_el)
                triggers.append(new_trigger)
        return triggers

    @staticmethod
    def _get_random_wake_up_answers(settings):
        """
        Return a list of the wake up answers set up on the settings.yml file

        :param settings: The YAML settings file
        :type settings: dict
        :return: List of wake up answers
        :rtype: list of str

        :Example:

            wakeup = cls._get_random_wake_up_answers(settings)

        .. seealso::
        .. raises:: NullSettingException
        .. warnings:: Class Method and Private
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

    @staticmethod
    def _get_random_wake_up_sounds(settings):
        """
        Return a list of the wake up sounds set up on the settings.yml file

        :param settings: The YAML settings file
        :type settings: dict
        :return: list of wake up sounds
        :rtype: list of str

        :Example:

            wakeup_sounds = cls._get_random_wake_up_sounds(settings)

        .. seealso::
        .. raises:: NullSettingException
        .. warnings:: Class Method and Private
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

    @staticmethod
    def _get_rest_api(settings):
        """
        Return the settings of the RestApi

        :param settings: The YAML settings file
        :type settings: dict
        :return: the RestApi object
        :rtype: RestApi

        :Example:

            rest_api = cls._get_rest_api(settings)

        .. seealso:: RestApi
        .. raises:: SettingNotFound, NullSettingException, SettingInvalidException
        .. warnings:: Class Method and Private
        """

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
            rest_api_obj = RestAPI(password_protected=password_protected, login=login, password=password,
                                   active=active, port=port)
            return rest_api_obj
        else:
            raise NullSettingException("rest_api settings cannot be null")

    @staticmethod
    def _get_cache_path(settings):
        """
        Return the path where to store the cache

        :param settings: The YAML settings file
        :type settings: dict
        :return: the path to store the cache
        :rtype: String

        :Example:

            cache_path = cls._get_cache_path(settings)

        .. seealso::
        .. raises:: SettingNotFound, NullSettingException, SettingInvalidException
        .. warnings:: Class Method and Private
        """

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

    @staticmethod
    def _get_default_synapse(settings):
        """
        Return the name of the default synapse

        :param settings: The YAML settings file
        :type settings: dict
        :return: the default synapse name
        :rtype: String

        :Example:

            default_synapse = cls._get_default_synapse(settings)

        .. seealso::
        .. raises:: SettingNotFound, NullSettingException, SettingInvalidException
        .. warnings:: Class Method and Private
        """

        try:
            default_synapse = settings["default_synapse"]
            logger.debug("Default synapse: %s" % default_synapse)
        except KeyError:
            default_synapse = None

        return default_synapse

    @staticmethod
    def _get_resources(settings):
        """
        Return a resources object that contains path of third party modules

        :param settings: The YAML settings file
        :type settings: dict
        :return: the resource object
        :rtype: Resources

        :Example:

            resource_directory = cls._get_resource_dir(settings)

        .. seealso::
        .. raises:: SettingNotFound, NullSettingException, SettingInvalidException
        .. warnings:: Class Method and Private
        """
        try:
            resource_dir = settings["resource_directory"]
            logger.debug("Resource directory synapse: %s" % resource_dir)

            neuron_folder = None
            stt_folder = None
            tts_folder = None
            trigger_folder = None
            if "neuron" in resource_dir:
                neuron_folder = resource_dir["neuron"]
                if not os.path.exists(neuron_folder):
                    raise SettingInvalidException("The path %s does not exist on the system" % neuron_folder)

            if "stt" in resource_dir:
                stt_folder = resource_dir["stt"]
                if not os.path.exists(stt_folder):
                    raise SettingInvalidException("The path %s does not exist on the system" % stt_folder)

            if "tts" in resource_dir:
                tts_folder = resource_dir["tts"]
                if not os.path.exists(tts_folder):
                    raise SettingInvalidException("The path %s does not exist on the system" % tts_folder)

            if "trigger" in resource_dir:
                trigger_folder = resource_dir["trigger"]
                if not os.path.exists(trigger_folder):
                    raise SettingInvalidException("The path %s does not exist on the system" % trigger_folder)

            if neuron_folder is None \
                    and stt_folder is None \
                    and tts_folder is None \
                    and trigger_folder is None:
                raise SettingInvalidException("No required folder has been provided in the setting resource_directory. "
                                              "Define : \'neuron\' or/and \'stt\' or/and \'tts\' or/and \'trigger\'")

            resource_object = Resources(neuron_folder=neuron_folder,
                                        stt_folder=stt_folder,
                                        tts_folder=tts_folder,
                                        trigger_folder=trigger_folder)
        except KeyError:
            logger.debug("Resource directory not found in settings")
            resource_object = None

        return resource_object


