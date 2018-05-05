class Synapse(object):
    """
    This Class is representing a Synapse with its name, and a dict of Neurons and a dict of signals

    .. note:: must be defined in the brain.yml
    """

    def __init__(self, name=None, neurons=None, signals=None, enabled=True):
        self.name = name
        self.neurons = neurons
        self.signals = signals
        self.enabled = enabled

    def serialize(self):
        """
        This method allows to serialize in a proper way this object

        :return: A dict of name, neurons, signals
        :rtype: Dict
        """

        return {
            'name': self.name,
            'neurons': [e.serialize() for e in self.neurons],
            'signals': [e.serialize() for e in self.signals],
            'enabled': self.enabled
        }

    def __str__(self):
        return str(self.serialize())

    def __eq__(self, other):
        """
        This is used to compare 2 objects
        :param other:
        :return:
        """
        return self.__dict__ == other.__dict__
