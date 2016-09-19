from BrainLoader import BrainLoader
from SettingLoader import SettingLoader


class ConfigurationManager:

    def __init__(self):
        BRAIN_FILE_NAME = "brain.yml"
        SETTING_FILE_NAME = "settings.yml"
        self.brainLoader = BrainLoader(BRAIN_FILE_NAME)
        self.settingLoader = SettingLoader(SETTING_FILE_NAME)
