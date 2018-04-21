class SettingsEntry(object):
    """
    This is an interface representing an entry in the settings file
    """

    def __init__(self, name=None):
        self.name = name

    def __str__(self):
        return str(self.serialize())

    def serialize(self):
        return {
            'name': self.name
        }

    def __eq__(self, other):
        """
        This is used to compare 2 objects
        :param other:
        :return:
        """
        return self.__dict__ == other.__dict__
