import logging

from kalliope.core.Utils import Utils
from kalliope.core.HookManager import HookManager
from kalliope.core.ConfigurationManager import SettingLoader

logging.basicConfig()
logger = logging.getLogger("kalliope")


class SettingEditor(object):
    """This Static class provides methods/functions to update properties from the Settings"""

    @staticmethod
    def _check_name_in_list_settings_entry(name_to_check, list_settings_entry):
        """
        manage object models : STT, TRIGGERS, TTS, PLAYERS because they have "name" attributes
        :param name_to_check: name to find in the list_settings_entry ~kalliope.core.Models.settings.SettingsEntry.SettingsEntry
        :param list_settings_entry: the list of SettingsEntry to inspect
        :return: True if the name_to_check corresponds to a name in the SettingsEntry list provided.
        """
        found = False
        for settings_entry in list_settings_entry:
            if settings_entry.name == name_to_check:
                found = True
                break
        return found

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
    @classmethod
    def set_default_player(cls, default_player_name):
        """
        Set dynamically a new default_player in the settings
        :param default_player_name: string value
        """
        settings = SettingLoader().settings
        if cls._check_name_in_list_settings_entry(default_player_name, settings.players):
            settings.default_player_name = default_player_name
        else:
            logger.debug("[Settings] default_player %s is not defined in settings file ", default_player_name)

    @staticmethod
    def set_players(new_player):
        """
        Add a new Player object in the list of players in the settings.
        If PLayer already exists in settings, it will be updated with the new player provided values.
        :param new_player: the new PLayer object to add in the settings.
        """
        settings = SettingLoader().settings
        list_no_duplicate_player = [player for player in settings.players if player.name != new_player.name]
        list_no_duplicate_player.append(new_player)
        settings.players = list_no_duplicate_player

    # TTS
    @classmethod
    def set_default_tts(cls, default_tts_name):
        """
        Set dynamically a new default_tts_name in the settings
        :param default_tts_name: string value
        """
        settings = SettingLoader().settings
        # Verify that the default name exists in the settings list
        if cls._check_name_in_list_settings_entry(default_tts_name, settings.ttss):
            settings.default_tts_name = default_tts_name
        else:
            logger.debug("[SettingsEditor] default_tts %s is not defined in settings file ", default_tts_name)

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
    @classmethod
    def set_default_stt(cls, default_stt_name):
        """
        Set dynamically a new default_stt_name in the settings if in the list of stts.
        :param default_stt_name: string value
        """
        settings = SettingLoader().settings
        if cls._check_name_in_list_settings_entry(default_stt_name, settings.stts):
            settings.default_stt_name = default_stt_name
        else:
            logger.debug("[Settings] default_stt %s is not defined in settings file ", default_stt_name)

    @staticmethod
    def set_stts(new_stt):
        """
        Add or update the speak to text list defined in the settings.
        :param new_stt: The new stt instance.
        """
        settings = SettingLoader().settings
        list_no_duplicate_stt = [stt for stt in settings.stts if stt.name != new_stt.name]
        list_no_duplicate_stt.append(new_stt)
        settings.stts = list_no_duplicate_stt

    # TRIGGER
    @classmethod
    def set_default_trigger(cls, default_trigger):
        """
        Set dynamically a new default_trigger in the settingss
        :param default_trigger: string value
        """
        settings = SettingLoader().settings
        if cls._check_name_in_list_settings_entry(default_trigger, settings.triggers):
            settings.default_trigger_name = default_trigger
        else:
            logger.debug("[Settings] default_trigger %s is not defined in settings file ", default_trigger)

    @staticmethod
    def set_trigger(new_trigger):
        """
        Update the list of triggers with a new trigger instance.
        If the trigger name already exists then it will be updated otherwise it will be added.
        :param new_trigger: the new trigger instance
        """
        settings = SettingLoader().settings
        list_no_duplicate_triggers = [trigger for trigger in settings.triggers if trigger.name != new_trigger.name]
        list_no_duplicate_triggers.append(new_trigger)
        settings.triggers = list_no_duplicate_triggers

    # HOOKS
    @staticmethod
    def set_hooks(hooks):
        """
        Update the hooks dictionary defined in the settings with the new dictionary in param.
        :param hooks: the dictionary containing hooks to update.
        :type hooks : dict
        """
        settings = SettingLoader().settings
        settings.hooks.update(hooks)

    # Variables
    @staticmethod
    def set_variables(variables):
        """
        Update the settings variables dictionary.
        :param variables: The dict of variables with the new values.
        """
        settings = SettingLoader().settings
        settings.variables.update(variables)
