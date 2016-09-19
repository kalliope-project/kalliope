from BrainLoader import BrainLoader
from SettingLoader import SettingLoader

class ConfigurationManager() :

    BRAIN_FILE_NAME = "brain.yml"
    SETTING_FILE_NAME = "settings.yml"

    def __init__(self):
        self.brainLoader = BrainLoader(self.BRAIN_FILE_NAME)
        self.settingLoader = SettingLoader(self.SETTING_FILE_NAME)
