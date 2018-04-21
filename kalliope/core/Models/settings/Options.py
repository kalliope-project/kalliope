from kalliope.core.Models.settings.SettingsEntry import SettingsEntry


class Options(SettingsEntry):
    """
    This Class is representing an Option element with parameters and values

    .. note:: must be defined in the settings.yml
    """

    def __init__(self, energy_threshold=4000, adjust_for_ambient_noise_second=0, deaf=None, mute=None):
        super(Options, self).__init__(name="Options")
        self.deaf = deaf
        self.mute = mute
        self.energy_threshold = energy_threshold
        self.adjust_for_ambient_noise_second = adjust_for_ambient_noise_second

    def __str__(self):
        return str(self.serialize())

    def serialize(self):
        return {
            'name': self.name,
            'energy_threshold': self.energy_threshold,
            'adjust_for_ambient_noise_second': self.adjust_for_ambient_noise_second,
            'deaf': self.deaf,
            'mute': self.mute
        }

    def __eq__(self, other):
        """
        This is used to compare 2 objects
        :param other: the Options to compare
        :return: True if both Options are similar, False otherwise
        """
        return self.__dict__ == other.__dict__
