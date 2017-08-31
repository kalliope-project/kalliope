class Signal(object):
    """
    This Class is representing a Signal which is corresponding to an input action that should start executing neuron
    list when triggered
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
        """
        Return a string that describe the signal. If a parameter contains the word "password",
        the output of this parameter will be masked in order to not appears in clean in the console
        :return: string description of the neuron
        """
        returned_dict = {
            'name': self.name,
            'parameters': self.parameters
        }

        cleaned_parameters = dict()
        if isinstance(self.parameters, dict):
            for key, value in self.parameters.items():
                if "password" in key:
                    cleaned_parameters[key] = "*****"
                else:
                    cleaned_parameters[key] = value
            returned_dict["parameters"] = cleaned_parameters

        return str(returned_dict)

    def __eq__(self, other):
        """
        This is used to compare 2 objects
        :param other:
        :return:
        """
        return self.__dict__ == other.__dict__
