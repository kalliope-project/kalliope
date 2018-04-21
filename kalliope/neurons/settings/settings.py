import logging

from kalliope import SignalLauncher
from kalliope.core import NeuronModule
from kalliope.core.ConfigurationManager import SettingEditor
from kalliope.core.Models.settings.Tts import Tts

logging.basicConfig()
logger = logging.getLogger("kalliope")


class Settings(NeuronModule):
    """
    """

    def __init__(self, **kwargs):
        super(Settings, self).__init__(**kwargs)

        self.default_tts_name = kwargs.get("default_tts_name", None)
        self.tts = kwargs.get("tts", None)

        self.default_stt_name = kwargs.get("default_stt_name", None)
        self.default_trigger_name = kwargs.get("default_trigger_name", None)
        self.default_player_name = kwargs.get("default_player_name", None)

        self.deaf = kwargs.get("deaf", None)
        self.mute = kwargs.get("mute", None)
        self.energy_threshold = kwargs.get("energy_threshold", None)
        self.adjust_for_ambient_noise_second = kwargs.get("adjust_for_ambient_noise_second", None)

        if self._is_parameters_ok():
            self._set_settings()

    def _is_parameters_ok(self):
        """
        Check the validity for each parameter
        :return: True if all parameters are set correctly, False otherwise.
        """

        # Players
        if self.default_player_name:
            if not self._check_name_in_list_settings_entry(self.default_player_name, self.settings.players):
                logger.debug("[Settings] default_player_name %s is not defined in settings file ",
                             self.default_player_name)
                return False

        # STT
        if self.default_stt_name:
            if not self._check_name_in_list_settings_entry(self.default_stt_name, self.settings.stts):
                logger.debug("[Settings] default_stt_name %s is not defined in settings file ", self.default_stt_name)
                return False

        # TRIGGER
        if self.default_trigger_name:
            if self._check_name_in_list_settings_entry(self.default_trigger_name, self.settings.triggers):
                logger.debug("[Settings] default_trigger_name %s is not defined in settings file ",
                             self.default_trigger_name)
                return False

        # TTS
        if self.default_tts_name:
            if not self._check_name_in_list_settings_entry(self.default_tts_name, self.settings.ttss):
                logger.debug("[Settings] default_tts_name %s is not defined in settings file ", self.default_tts_name)
                return False
        # TODO remove TTS management from the NeuronModule class
        if self.tts:
            if not isinstance(self.tts, list):
                logger.debug("[Settings] tts current type: %s. tts should be a list", type(self.tts))
                return False
            for tts_el in self.tts:
                if not isinstance(tts_el, dict):
                    logger.debug("[Settings] tts element current type: %s. tts element should be a dict", type(tts_el))
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

        # TODO HOOKS

        # TODO Resources

        # TODO REST API

        # TODO Variables

        return True

    def _set_settings(self):
        if self.default_player_name:
            SettingEditor.set_default_player_name(self.default_player_name)

        if self.default_stt_name:
            SettingEditor.set_default_stt_name(self.default_stt_name)

        if self.default_trigger_name:
            SettingEditor.set_default_trigger_name(self.default_trigger_name)

        if self.default_tts_name:
            SettingEditor.set_default_tts_name(self.default_tts_name)

        if self.tts:
            for tts_el in self.tts:
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
