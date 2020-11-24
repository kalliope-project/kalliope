import logging
import os
import uuid

from six import with_metaclass

from kalliope.core.Models.settings.Options import Options
from .YAMLLoader import YAMLLoader
from kalliope.core.Models.settings.Resources import Resources
from kalliope.core.Utils.Utils import Utils
from kalliope.core.Models import Singleton
from kalliope.core.Models.settings.RestAPI import RestAPI
from kalliope.core.Models.settings.Settings import Settings
from kalliope.core.Models.settings.Stt import Stt
from kalliope.core.Models.settings.Trigger import Trigger
from kalliope.core.Models.settings.Player import Player
from kalliope.core.Models.settings.Tts import Tts
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


class SettingLoader(with_metaclass(Singleton, object)):
    """
    This Class is used to get the Settings YAML and the Settings as an object
    """

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
        default_player_name = self._get_default_player(settings)
        stts = self._get_stts(settings)
        ttss = self._get_ttss(settings)
        triggers = self._get_triggers(settings)
        players = self._get_players(settings)
        rest_api = self._get_rest_api(settings)
        cache_path = self._get_cache_path(settings)
        resources = self._get_resources(settings)
        variables = self._get_variables(settings)
        options = self._get_options(settings)
        hooks = self._get_hooks(settings)
        tracker_anonymous_usage_stats_id = self._get_anonymous_usage_stats(settings)

        # Load the setting singleton with the parameters
        setting_object.default_tts_name = default_tts_name
        setting_object.default_stt_name = default_stt_name
        setting_object.default_trigger_name = default_trigger_name
        setting_object.default_player_name = default_player_name
        setting_object.stts = stts
        setting_object.ttss = ttss
        setting_object.triggers = triggers
        setting_object.players = players
        setting_object.rest_api = rest_api
        setting_object.cache_path = cache_path
        setting_object.resources = resources
        setting_object.variables = variables
        setting_object.options = options
        setting_object.hooks = hooks
        setting_object.tracker_anonymous_usage_stats_id = tracker_anonymous_usage_stats_id

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
        except KeyError as e:
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
        except KeyError as e:
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
        except KeyError as e:
            raise SettingNotFound("%s setting not found" % e)

    @staticmethod
    def _get_default_player(settings):
        """
        Get the default player defined in the settings.yml file
        :param settings: The YAML settings file
        :type settings: dict
        :return: the default player
        :rtype: str

        :Example:

            default_player_name = cls._get_default_player(settings)

        .. seealso:: Player
        .. raises:: NullSettingException, SettingNotFound
        .. warnings:: Static and Private
        """

        try:
            default_player = settings["default_player"]
            if default_player is None:
                raise NullSettingException("Attribute default_player is null")
            logger.debug("Default Player name: %s" % default_player)
            return default_player
        except KeyError as e:
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
        .. warnings:: Static Method and Private
        """

        try:
            speechs_to_text_list = settings["speech_to_text"]
        except KeyError:
            raise SettingNotFound("speech_to_text settings not found")

        stts = list()
        for speechs_to_text_el in speechs_to_text_list:
            if isinstance(speechs_to_text_el, dict):
                for stt_name in speechs_to_text_el:
                    name = stt_name
                    parameters = speechs_to_text_el[name]
                    new_stt = Stt(name=name, parameters=parameters)
                    stts.append(new_stt)
            else:
                # the stt does not have parameter
                new_stt = Stt(name=speechs_to_text_el, parameters=dict())
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
        .. warnings:: Static Method and Private
        """

        try:
            text_to_speech_list = settings["text_to_speech"]
        except KeyError as e:
            raise SettingNotFound("%s setting not found" % e)

        ttss = list()
        for text_to_speech_el in text_to_speech_list:
            if isinstance(text_to_speech_el, dict):
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
        .. warnings:: Static Method and Private
        """

        try:
            triggers_list = settings["triggers"]
        except KeyError as e:
            raise SettingNotFound("%s setting not found" % e)

        triggers = list()
        for trigger_el in triggers_list:
            if isinstance(trigger_el, dict):
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
    def _get_players(settings):
        """
        Return a list of Player object

        :param settings: The YAML settings file
        :type settings: dict
        :return: List of Player
        :rtype: list

        :Example:

            players = cls._get_players(settings)

        .. seealso:: players
        .. raises:: SettingNotFound
        .. warnings:: Static Method and Private
        """

        try:
            players_list = settings["players"]
        except KeyError as e:
            raise SettingNotFound("%s setting not found" % e)

        players = list()
        for player_el in players_list:
            if isinstance(player_el, dict):
                for player_name in player_el:
                    name = player_name
                    parameters = player_el[name]
                    new_player = Player(name=name, parameters=parameters)
                    players.append(new_player)
            else:
                # the player does not have parameters
                new_player = Player(name=player_el)
                players.append(new_player)
        return players

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
        except KeyError as e:
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
                    if password is None:
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

                # check the CORS request settings
                allowed_cors_origin = False
                if "allowed_cors_origin" in rest_api:
                    allowed_cors_origin = rest_api["allowed_cors_origin"]

            except KeyError as e:
                raise SettingNotFound("%s settings not found" % e)

            # config ok, we can return the rest api object
            rest_api_obj = RestAPI(password_protected=password_protected, login=login, password=password,
                                   active=active, port=port, allowed_cors_origin=allowed_cors_origin)
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
        except KeyError as e:
            raise SettingNotFound("%s setting not found" % e)

        if cache_path is None:
            raise NullSettingException("cache_path setting cannot be null")

        # test if that path is usable
        if FileManager.is_path_exists_or_creatable(cache_path):
            return cache_path
        else:
            raise SettingInvalidException("The cache_path seems to be invalid: %s" % cache_path)

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
        # return an empty resource object anyway
        resource_object = Resources()
        try:
            resource_dir = settings["resource_directory"]
            logger.debug("Resource directory synapse: %s" % resource_dir)

            neuron_folder = None
            stt_folder = None
            tts_folder = None
            trigger_folder = None
            signal_folder = None

            if "neuron" in resource_dir:
                neuron_folder = resource_dir["neuron"]
                if os.path.exists(neuron_folder):
                    logger.debug("[SettingLoader] Neuron resource folder path loaded: %s" % neuron_folder)
                    resource_object.neuron_folder = neuron_folder
                else:
                    raise SettingInvalidException("The path %s does not exist on the system" % neuron_folder)

            if "stt" in resource_dir:
                stt_folder = resource_dir["stt"]
                if os.path.exists(stt_folder):
                    logger.debug("[SettingLoader] STT resource folder path loaded: %s" % stt_folder)
                    resource_object.stt_folder = stt_folder
                else:
                    raise SettingInvalidException("The path %s does not exist on the system" % stt_folder)

            if "tts" in resource_dir:
                tts_folder = resource_dir["tts"]
                if os.path.exists(tts_folder):
                    logger.debug("[SettingLoader] TTS resource folder path loaded: %s" % tts_folder)
                    resource_object.tts_folder = tts_folder
                else:
                    raise SettingInvalidException("The path %s does not exist on the system" % tts_folder)

            if "trigger" in resource_dir:
                trigger_folder = resource_dir["trigger"]
                if os.path.exists(trigger_folder):
                    logger.debug("[SettingLoader] Trigger resource folder path loaded: %s" % trigger_folder)
                    resource_object.trigger_folder = trigger_folder
                else:
                    raise SettingInvalidException("The path %s does not exist on the system" % trigger_folder)

            if "signal" in resource_dir:
                signal_folder = resource_dir["signal"]
                if os.path.exists(signal_folder):
                    logger.debug("[SettingLoader] Signal resource folder path loaded: %s" % signal_folder)
                    resource_object.signal_folder = signal_folder
                else:
                    raise SettingInvalidException("The path %s does not exist on the system" % signal_folder)

            if neuron_folder is None \
                    and stt_folder is None \
                    and tts_folder is None \
                    and trigger_folder is None \
                    and signal_folder is None:
                raise SettingInvalidException("No required folder has been provided in the setting resource_directory. "
                                              "Define : \'neuron\' or/and \'stt\' or/and \'tts\' or/and \'trigger\' "
                                              "or/and \'signal\'")

        except KeyError:
            logger.debug("Resource directory not found in settings")
            return resource_object

        return resource_object

    @staticmethod
    def _get_variables(settings):
        """
        Return the dict of variables from the settings.
        :param settings: The YAML settings file
        :return: dict
        """

        variables = dict()
        try:
            variables_files_name = settings["var_files"]
            # In case files are declared in settings.yml, make sure kalliope can access them.
            for files in variables_files_name:
                var = Utils.get_real_file_path(files)
                if var is None:
                    raise SettingInvalidException("Variables file %s not found" % files)
                else:
                    variables.update(YAMLLoader.get_config(var))
            return variables
        except KeyError:
            # User does not provide this settings
            return dict()

    @staticmethod
    def _get_options(settings):
        """
        Return the Options settings
        if not set, default values are :
        deaf: False
        mute: False
        energy_threshold = 4000
        adjust_for_ambient_noise_second = 0

        :param settings: The YAML settings file
        :type settings: dict
        :return: An Options with the start options
        :rtype: Options
        """

        deaf = False
        mute = False
        recognizer_multiplier = 1.0
        recognizer_energy_ratio = 1.5
        recognizer_recording_timeout = 15.0
        recognizer_recording_timeout_with_silence = 3.0

        try:
            options = settings["options"]
            if "deaf" in options:
                deaf = options['deaf']
            if "mute" in options:
                mute = options['mute']
            if "recognizer_multiplier" in options:
                recognizer_multiplier = options["recognizer_multiplier"]
            if "recognizer_energy_ratio" in options:
                recognizer_energy_ratio = options["recognizer_energy_ratio"]
            if "recognizer_recording_timeout" in options:
                recognizer_recording_timeout = options["recognizer_recording_timeout"]
            if "recognizer_recording_timeout_with_silence" in options:
                recognizer_recording_timeout_with_silence = options["recognizer_recording_timeout_with_silence"]
        except KeyError as e:
            logger.debug("[SettingsLoader] missing settings key: %s" % e)
            pass

        options = Options(recognizer_multiplier=recognizer_multiplier,
                          recognizer_energy_ratio=recognizer_energy_ratio,
                          recognizer_recording_timeout=recognizer_recording_timeout,
                          recognizer_recording_timeout_with_silence=recognizer_recording_timeout_with_silence,
                          deaf=deaf,
                          mute=mute)
        logger.debug("[SettingsLoader] Options: %s" % options)
        return options

    @staticmethod
    def _get_hooks(settings):
        """
        Return hooks settings
        :param settings: The YAML settings file
        :return: A dict containing hooks
        :rtype: dict
        """

        try:
            hooks = settings["hooks"]

        except KeyError:
            # if the user haven't set any hooks we define an empty dict
            hooks = dict()

        all_hook = [
            "on_start",
            "on_waiting_for_trigger",
            "on_triggered",
            "on_start_listening",
            "on_stop_listening",
            "on_order_found",
            "on_order_not_found",
            "on_deaf",
            "on_undeaf",
            "on_mute",
            "on_unmute",
            "on_start_speaking",
            "on_stop_speaking"
        ]

        for key in all_hook:
            if key not in hooks:
                hooks[key] = None

        return hooks

    @staticmethod
    def _get_anonymous_usage_stats(settings):
        cid = uuid.uuid4().hex
        try:
            send_anonymous_usage_stats = settings["send_anonymous_usage_stats"]
            bool_send_anonymous_usage_stats = Utils.str_to_bool(send_anonymous_usage_stats)
            if bool_send_anonymous_usage_stats:
                # generate a unique user ID
                send_anonymous_usage_stats = cid
            else:  # the user choose to disable stats
                send_anonymous_usage_stats = "not_defined_id"

        except KeyError:
            # if the user haven't set this flag we default to silent
            send_anonymous_usage_stats = "not_defined_id"
        logger.debug("[SettingsLoader] send_anonymous_usage_stats: %s" % send_anonymous_usage_stats)
        return send_anonymous_usage_stats
