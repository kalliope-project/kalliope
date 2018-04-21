import logging

from kalliope.core.Utils import Utils
from kalliope.core.HookManager import HookManager
from kalliope.core.ConfigurationManager import SettingLoader

logging.basicConfig()
logger = logging.getLogger("kalliope")


class SettingEditor(object):
    """This class provides methods/functions to update properties from the Settings"""

    # Options
    @staticmethod
    def set_mute_status(mute=False):
        """
        Define is the mute status
        :param mute: Boolean. If false, Kalliope is voice is stopped
        """
        logger.debug("[SettingEditor] mute. Switch trigger process to mute : %s" % mute)
        settings = SettingLoader().settings
        if mute:
            Utils.print_info("Kalliope now muted, voice has been stopped.")
            HookManager.on_mute()
        else:
            Utils.print_info("Kalliope now speaking.")
            HookManager.on_unmute()
        settings.options.mute = mute

    @staticmethod
    def set_deaf_status(trigger_instance, deaf=False):
        """
        Define is the trigger is listening or not.
        :param trigger_instance: the trigger instance coming from the order. It will be paused or unpaused.
        :param deaf: Boolean. If true, kalliope is trigger is paused
        """
        logger.debug("[MainController] deaf . Switch trigger process to deaf : %s" % deaf)
        settings = SettingLoader().settings
        if deaf:
            trigger_instance.pause()
            Utils.print_info("Kalliope now deaf, trigger has been paused")
            HookManager.on_deaf()
        else:
            trigger_instance.unpause()
            Utils.print_info("Kalliope now listening for trigger detection")
            HookManager.on_undeaf()
        settings.options.deaf = deaf

    @staticmethod
    def set_adjust_for_ambient_noise_second(adjust_for_ambient_noise_second):
        """
        Set a new value for the adjust_for_ambient_noise_second;
        Must be an integer.
        :param adjust_for_ambient_noise_second: new value to push to the adjust_for_ambient_noise_second in the Options settings
        """
        if isinstance(adjust_for_ambient_noise_second, int):
            settings = SettingLoader().settings
            settings.options.adjust_for_ambient_noise_second = adjust_for_ambient_noise_second

    @staticmethod
    def set_energy_threshold(energy_threshold):
        """
        Set the new value of the energy threshold to the settings.
        Must be an integer.
        :param energy_threshold: new value for the energy_threshold to push into the settings
        """
        if isinstance(energy_threshold, int):
            settings = SettingLoader().settings
            settings.options.energy_threshold = energy_threshold

    # Players
    @staticmethod
    def set_default_player_name(default_player_name):
        """
        Set dynamically a new default_player in the settings
        :param default_player_name: string value
        """
        settings = SettingLoader().settings
        settings.default_player_name = default_player_name

    # TTS
    @staticmethod
    def set_default_tts_name(default_tts_name):
        """
        Set dynamically a new default_tts_name in the settings
        :param default_tts_name: string value
        """
        settings = SettingLoader().settings
        settings.default_tts_name = default_tts_name

    @staticmethod
    def set_ttss(new_tts):
        """
        Add a new TTS object in the list of tts in the settings.
        If TTS already exists in settings, it will be updated with the new tts provided values.
        :param new_tts: the new TTS object to add in the settings.
        """
        settings = SettingLoader().settings
        list_no_duplicate_tts = [tts for tts in settings.ttss if tts.name != new_tts.name]
        list_no_duplicate_tts.append(new_tts)
        settings.ttss = list_no_duplicate_tts

    # STT
    @staticmethod
    def set_default_stt_name(default_stt_name):
        """
        Set dynamically a new default_stt_name in the settings
        :param default_stt_name: string value
        """
        settings = SettingLoader().settings
        settings.default_stt_name = default_stt_name

    # TRIGGER
    @staticmethod
    def set_default_trigger_name(default_trigger_name):
        """
        Set dynamically a new default_trigger_name in the settingss
        :param default_trigger_name: string value
        """
        settings = SettingLoader().settings
        settings.default_trigger_name = default_trigger_name
