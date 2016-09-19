from YAMLLoader import yamlloader

class BrainLoader(yamlloader):

    FILE_NAME = "brain.yml"

    def __init__(self):
        self.fileName =  self.FILE_NAME
        self.filePath = "../../" + self.fileName
        yamlloader.__init__(self, self.filePath)

    def __init__(self, filename):
        self.fileName = filename;
        self.filePath = "../../" + self.fileName
        yamlloader.__init__(self, self.filePath)

    def get_config(self):
        return yamlloader.get_config(self)



