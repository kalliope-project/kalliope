class SttOptions(object):
    """
    This Class is representing a Speech To Text (STT) element with name and parameters

    .. note:: must be defined in the settings.yml
    """

    def __init__(self, energy_threshold=4000, adjust_for_ambient_noise_second=0):
        self.energy_threshold = energy_threshold
        self.adjust_for_ambient_noise_second = adjust_for_ambient_noise_second

    def __str__(self):
        return str(self.serialize())

    def serialize(self):
        return {
            'energy_threshold': self.energy_threshold,
            'adjust_for_ambient_noise_second': self.adjust_for_ambient_noise_second
        }

    def __eq__(self, other):
        """
        This is used to compare 2 objects
        :param other:
        :return:
        """
        return self.__dict__ == other.__dict__
