class Trigger(object):
    """
    This Class is representing a Trigger with its name and parameters

    .. note:: must be defined in the settings.yml
    """

    def __init__(self, name=None, parameters=None):
        self.name = name
        self.parameters = parameters

    def __str__(self):
        return "Trigger name: %s, parameters: %s" % (str(self.name), str(self.parameters))
