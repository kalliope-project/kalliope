import logging

from kalliope import SignalLauncher
from kalliope.core import NeuronModule
from kalliope.core.ConfigurationManager import SettingEditor

logging.basicConfig()
logger = logging.getLogger("kalliope")


class Settings(NeuronModule):
    """
    TODO : manage update dynamic list of the stts, ttss, triggers, etc ...
    """

    def __init__(self, **kwargs):
        super(Settings, self).__init__(**kwargs)

        self.default_tts_name = kwargs.get("default_tts_name", None)
        self.default_stt_name = kwargs.get("default_stt_name", None)
        self.default_trigger_name = kwargs.get("default_trigger_name", None)
        self.default_player_name = kwargs.get("default_player_name", None)
        self.deaf = kwargs.get("deaf", None)
        self.mute = kwargs.get("mute", None)

        if self._is_parameters_ok():
            self._set_settings()

    def _is_parameters_ok(self):
        """
        Check the validity for each parameter
        :return: True if all parameters are set correctly, False otherwise.
        """
        if self.default_player_name:
            if not self._check_name_in_list_settings_entry(self.default_player_name, self.settings.players):
                logger.debug("[Settings] default_player_name %s is not defined in settings file ",
                             self.default_player_name)
                return False

        if self.default_stt_name:
            if not self._check_name_in_list_settings_entry(self.default_stt_name, self.settings.stts):
                logger.debug("[Settings] default_stt_name %s is not defined in settings file ", self.default_stt_name)
                return False

        if self.default_trigger_name:
            if self._check_name_in_list_settings_entry(self.default_trigger_name, self.settings.triggers):
                logger.debug("[Settings] default_trigger_name %s is not defined in settings file ",
                             self.default_trigger_name)
                return False

        if self.default_tts_name:
            if not self._check_name_in_list_settings_entry(self.default_tts_name, self.settings.ttss):
                logger.debug("[Settings] default_tts_name %s is not defined in settings file ", self.default_tts_name)
                return False

        if self.deaf is not None:
            if not isinstance(self.deaf, bool):
                logger.debug("[Settings] deaf %s is not a correct value, you must define True or False", self.deaf)
                return False

        if self.mute is not None:
            if not isinstance(self.mute, bool):
                logger.debug("[Settings] mute %s is not a correct value, you must define True or False", self.mute)
                return False

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

        if self.deaf is not None:
            signal_order = SignalLauncher.get_order_instance()
            if signal_order is not None:
                SettingEditor.set_deaf_status(signal_order.trigger_instance, self.status)

        if self.mute is not None:
            SettingEditor.set_mute_status(self.mute)

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