class Synapse(object):
    """
    This Class is representing a Synapse with its name, and a dict of Neurons and a dict of signals

    .. note:: must be defined in the brain.yml
    """

    def __init__(self, name=None, neurons=None, signals=None):
        self.name = name
        self.neurons = neurons
        self.signals = signals

    def serialize(self):
        """
        This method allows to serialize in a proper way this object

        :return: A dict of name, neurons, signals
        :rtype: Dict
        """

        return {
            'name': self.name,
            'neurons': [e.serialize() for e in self.neurons],
            'signals': [e.serialize() for e in self.signals]
        }

    def __str__(self):
        return_val = "Synapse name: %s" % self.name
        return_val += "\nneurons:"
        for el in self.neurons:
            return_val += str(el)
        return_val += "\nsignals:"
        for el in self.signals:
            return_val += str(el)
        return return_val

    def __eq__(self, other):
        """
        This is used to compare 2 objects
        :param other:
        :return:
        """
        return self.__dict__ == other.__dict__
