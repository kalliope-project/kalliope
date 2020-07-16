from kalliope.core.Models.settings.SettingsEntry import SettingsEntry


class Options(SettingsEntry):
    """
    This Class is representing an Option element with parameters and values

    .. note:: must be defined in the settings.yml
    """

    def __init__(self, 
                 recognizer_multiplier=1, 
                 recognizer_energy_ratio=1.5, 
                 recognizer_recording_timeout=15.0, 
                 recognizer_recording_timeout_with_silence=3.0, 
                 deaf=None, 
                 mute=None):
    
        super(Options, self).__init__(name="Options")
        self.deaf = deaf
        self.mute = mute
        self.recognizer_multiplier = recognizer_multiplier
        self.recognizer_energy_ratio = recognizer_energy_ratio
        self.recognizer_recording_timeout = recognizer_recording_timeout
        self.recognizer_recording_timeout_with_silence = recognizer_recording_timeout_with_silence

    def __str__(self):
        return str(self.serialize())

    def serialize(self):
        return {
            'name': self.name,
            'recognizer_multiplier': self.recognizer_multiplier,
            'recognizer_energy_ratio': self.recognizer_energy_ratio,
            'recognizer_recording_timeout': self.recognizer_recording_timeout,
            'recognizer_recording_timeout_with_silence': self.recognizer_recording_timeout_with_silence,
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