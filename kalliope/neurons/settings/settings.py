import logging

from kalliope import SignalLauncher, Utils
from kalliope.core import NeuronModule
from kalliope.core.ConfigurationManager import SettingEditor, YAMLLoader
from kalliope.core.Models.settings.Stt import Stt
from kalliope.core.Models.settings.Trigger import Trigger
from kalliope.core.Models.settings.Tts import Tts
from kalliope.core.Models.settings.Player import Player

logging.basicConfig()
logger = logging.getLogger("kalliope")


class Settings(NeuronModule):
    """

    """

    def __init__(self, **kwargs):
        super(Settings, self).__init__(**kwargs)

        # Modules
        self.default_tts = kwargs.get("default_tts", None)
        self.text_to_speech = kwargs.get("text_to_speech", None)

        self.default_stt = kwargs.get("default_stt", None)
        self.speech_to_text = kwargs.get("speech_to_text", None)

        self.default_trigger = kwargs.get("default_trigger", None)
        self.triggers = kwargs.get("triggers", None)

        self.default_player = kwargs.get("default_player", None)
        self.players = kwargs.get("players", None)

        # Options
        self.deaf = kwargs.get("deaf", None)
        self.mute = kwargs.get("mute", None)
        self.energy_threshold = kwargs.get("energy_threshold", None)
        self.adjust_for_ambient_noise_second = kwargs.get("adjust_for_ambient_noise_second", None)

        # Hooks
        self.hooks = kwargs.get("hooks", None)

        # Not applicable yet as Variables are applied during brainloading.
        # Variables
        # self.var_files = kwargs.get("var_files", None)

        # REST API
        # RESSOURCES ?

        if self._is_parameters_ok():
            self._set_settings()

    def _is_parameters_ok(self):
        """
        Check the validity for each parameter
        :return: True if all parameters are set correctly, False otherwise.
        """

        # Players
        if self.default_player:
            if not self._check_name_in_list_settings_entry(self.default_player, self.settings.players):
                logger.debug("[Settings] default_player %s is not defined in settings file ",
                             self.default_player)
                return False

        if self.players:
            if not isinstance(self.players, list):
                logger.debug("[Settings] players current type: %s. players should be a list", type(self.players))
                return False
            for player_el in self.players:
                if not isinstance(player_el, dict):
                    logger.debug("[Settings] player current element type: %s. player element should be a dict",
                                 type(player_el))
                    return False

        # STT
        if self.default_stt:
            if not self._check_name_in_list_settings_entry(self.default_stt, self.settings.stts):
                logger.debug("[Settings] default_stt %s is not defined in settings file ", self.default_stt)
                return False

        if self.speech_to_text:
            if not isinstance(self.speech_to_text, list):
                logger.debug("[Settings] speech_to_text current type: %s. speech_to_text should be a list",
                             type(self.speech_to_text))
                return False
            for stt_el in self.speech_to_text:
                if not isinstance(stt_el, dict):
                    logger.debug(
                        "[Settings] speech_to_text current element type: %s. speech_to_text element should be a dict",
                        type(stt_el))
                    return False

        # TRIGGER
        if self.default_trigger:
            if self._check_name_in_list_settings_entry(self.default_trigger, self.settings.triggers):
                logger.debug("[Settings] default_trigger %s is not defined in settings file ",
                             self.default_trigger)
                return False

        if self.triggers:
            if not isinstance(self.triggers, list):
                logger.debug("[Settings] triggers current type: %s. triggers should be a list", type(self.triggers))
                return False
            for trigger_el in self.triggers:
                if not isinstance(trigger_el, dict):
                    logger.debug("[Settings] triggers current element type: %s. triggers element should be a dict",
                                 type(trigger_el))
                    return False

        # TTS
        if self.default_tts:
            if not self._check_name_in_list_settings_entry(self.default_tts, self.settings.ttss):
                logger.debug("[Settings] default_tts %s is not defined in settings file ", self.default_tts)
                return False
        # TODO remove TTS management from the NeuronModule class
        if self.text_to_speech:
            if not isinstance(self.text_to_speech, list):
                logger.debug("[Settings] text_to_speech current type: %s. text_to_speech should be a list",
                             type(self.text_to_speech))
                return False
            for tts_el in self.text_to_speech:
                if not isinstance(tts_el, dict):
                    logger.debug(
                        "[Settings] text_to_speech element current type: %s. text_to_speech element should be a dict",
                        type(tts_el))
                    return False

        # Options
        if self.deaf is not None:
            if not isinstance(self.deaf, bool):
                logger.debug("[Settings] deaf %s is not a correct value, you must define True or False", self.deaf)
                return False

        if self.mute is not None:
            if not isinstance(self.mute, bool):
                logger.debug("[Settings] mute %s is not a correct value, you must define True or False", self.mute)
                return False

        if self.energy_threshold is not None:
            if not isinstance(self.energy_threshold, int):
                logger.debug("[Settings] energy_threshold %s is not a correct integer, you must define a number",
                             self.energy_threshold)
                return False

        if self.adjust_for_ambient_noise_second is not None:
            if not isinstance(self.adjust_for_ambient_noise_second, int):
                logger.debug(
                    "[Settings] adjust_for_ambient_noise_second %s is not a correct integer, you must define a number",
                    self.adjust_for_ambient_noise_second)
                return False

        # Hooks
        if self.hooks:
            if not isinstance(self.hooks, dict):
                logger.debug("[Settings] hooks property %s is not a dictionary as it should be.", type(self.hooks))
                return False
            for hook_name, synap in self.hooks.items():
                if not isinstance(synap, str) and not isinstance(synap, list):
                    logger.debug(
                        "[Settings] for hook element %s the type %s is nor a string nor a list as it should be.",
                        hook_name, type(synap))
                    return False

        # Variables
        if self.var_files:
            if not isinstance(self.var_files, list):
                logger.debug("[Settings] var_files property %s is not a list as it should be.", type(self.var_files))
                return False
            for file_name in self.var_files:
                var = Utils.get_real_file_path(file_name)
                if var is None:
                    logger.debug("[Settings] Variables file %s not found", file_name)
                    return False

        # TODO Resources Does it make sense to update this one ?

        # TODO REST API

        return True

    def _set_settings(self):
        # PLAYERS
        if self.default_player:
            SettingEditor.set_default_player(self.default_player)

        if self.players:
            for player_el in self.players:
                if isinstance(player_el, dict):
                    for player_name in player_el:
                        name = player_name
                        parameters = player_el[name]
                        new_player = Player(name=name, parameters=parameters)
                        SettingEditor.set_players(new_player)

        # STT
        if self.default_stt:
            SettingEditor.set_default_stt(self.default_stt)

        if self.speech_to_text:
            for stt_el in self.speech_to_text:
                if isinstance(stt_el, dict):
                    for stt_name in stt_el:
                        name = stt_name
                        parameters = stt_el[name]
                        new_stt = Stt(name=name, parameters=parameters)
                        SettingEditor.set_stts(new_stt)

        # TRIGGER
        if self.default_trigger:
            SettingEditor.set_default_trigger(self.default_trigger)

        if self.triggers:
            for trigger_el in self.triggers:
                if isinstance(trigger_el, dict):
                    for trigger_name in trigger_el:
                        name = trigger_name
                        parameters = trigger_el[name]
                        new_trigger = Trigger(name=name, parameters=parameters)
                        SettingEditor.set_trigger(new_trigger)

        # TTS
        if self.default_tts:
            SettingEditor.set_default_tts(self.default_tts)

        if self.text_to_speech:
            for tts_el in self.text_to_speech:
                if isinstance(tts_el, dict):
                    for tts_name in tts_el:
                        name = tts_name
                        parameters = tts_el[name]
                        new_tts = Tts(name=name, parameters=parameters)
                        SettingEditor.set_ttss(new_tts)

        # Options
        if self.deaf is not None:
            signal_order = SignalLauncher.get_order_instance()
            if signal_order is not None:
                SettingEditor.set_deaf_status(signal_order.trigger_instance, self.status)

        if self.mute is not None:
            SettingEditor.set_mute_status(self.mute)

        if self.energy_threshold is not None:
            SettingEditor.set_energy_threshold(self.energy_threshold)

        if self.adjust_for_ambient_noise_second is not None:
            SettingEditor.set_adjust_for_ambient_noise_second(self.adjust_for_ambient_noise_second)

        # Hooks
        if self.hooks:
            SettingEditor.set_hooks(self.hooks)

        # Variables
        if self.var_files:
            variables = dict()
            for files in self.var_files:
                var = Utils.get_real_file_path(files)
                # var is None has been checked previously in _is_parameters_ok() method
                variables.update(YAMLLoader.get_config(var))
            SettingEditor.set_variables(variables)

    @staticmethod
    def _check_name_in_list_settings_entry(name_to_check, list_settings_entry):
        """
        manage object models : STT, TRIGGERS, TTS, PLAYERS because they have "name" attributes
        TODO
        :param name_to_check:
        :param list_settings_entry:
        :return:
        """
        found = False
        for settings_entry in list_settings_entry:
            if settings_entry.name == name_to_check:
                found = True
        return found
