

class Resources(object):
    """

    """
    def __init__(self, neuron_folder=None, stt_folder=None, tts_folder=None, trigger_folder=None, signal_folder=None):
        self.neuron_folder = neuron_folder
        self.stt_folder = stt_folder
        self.tts_folder = tts_folder
        self.trigger_folder = trigger_folder
        self.signal_folder = signal_folder

    def __str__(self):
        return str(self.serialize())

    def serialize(self):
        """
        This method allows to serialize in a proper way this object

        :return: A dict of order
        :rtype: Dict
        """

        return {
            'neuron_folder': self.neuron_folder,
            'stt_folder': self.stt_folder,
            'tts_folder': self.tts_folder,
            'trigger_folder': self.trigger_folder,
            'signal_folder': self.signal_folder
        }

    def __eq__(self, other):
        """
        This is used to compare 2 objects
        :param other:
        :return:
        """
        return self.__dict__ == other.__dict__
