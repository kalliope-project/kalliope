class Stt(object):
    """
    This Class is representing a Speech To Text (STT) element with name and parameters

    .. note:: must be defined in the settings.yml
    """

    def __init__(self, name=None, parameters=None):
        self.name = name
        self.parameters = parameters

    def __str__(self):
        return "Stt name: %s, parameters: %s" % (str(self.name), str(self.parameters))

    def __eq__(self, other):
        """
        This is used to compare 2 objects
        :param other:
        :return:
        """
        return self.__dict__ == other.__dict__
