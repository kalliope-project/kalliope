from YAMLLoader import yamlloader

class SettingLoader(yamlloader) :

    FILE_NAME = "settings.yml"

    def __init__(self, yamlloader):
        self.fileName =  self.FILE_NAME;
        self.filePath = "../../" + self.fileName
        yamlloader.__init__(self, self.filePath)

    def get_config(self):
        return yamlloader.get_config(self)