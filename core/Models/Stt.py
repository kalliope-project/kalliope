

class Stt(object):
    def __init__(self, name=None, parameters=None):
        self.name = name
        self.parameters = parameters

    def __str__(self):
        return "Stt name: %s, parameters: %s" % (str(self.name), str(self.parameters))