from BrainLoader import BrainLoader
from SettingLoader import SettingLoader


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
