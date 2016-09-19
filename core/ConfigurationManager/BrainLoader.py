from YAMLLoader import YAMLLoader

FILE_NAME = "brain.yml"


class BrainLoader(YAMLLoader):

    def __init__(self, filename=None):
        self.fileName = filename
        if filename is None:
            self.fileName = FILE_NAME
        self.filePath = "../../" + self.fileName
        YAMLLoader.__init__(self, self.filePath)

    def get_config(self):
        return YAMLLoader.get_config(self)



