from BrainLoader import BrainLoader
from SettingLoader import SettingLoader


class ConfigurationManager:

    def __init__(self, brain_file_name=None, setting_file_name=None):
        if brain_file_name is None:
            brain_file_name = "brain.yml"
        if setting_file_name is None:
            setting_file_name = "settings.yml"
        self.brainLoader = BrainLoader(brain_file_name)
        self.settingLoader = SettingLoader(setting_file_name)
