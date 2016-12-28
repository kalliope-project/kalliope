class Neuron(object):
    """
    This Class is representing a Neuron which is corresponding to an action to perform.

    .. note:: Neurons are defined in the brain file
    """

    def __init__(self, name=None, parameters=None):
        self.name = name
        self.parameters = parameters

    def serialize(self):
        """
        This method allows to serialize in a proper way this object

        :return: A dict of name and parameters
        :rtype: Dict
        """
        return {
            'name': self.name,
            'parameters': self.parameters
        }

    def __str__(self):
        return "Neuron: name: %s, parameters: %s" % (self.name, self.parameters)

    def __eq__(self, other):
        """
        This is used to compare 2 objects
        :param other:
        :return:
        """
        return self.__dict__ == other.__dict__
