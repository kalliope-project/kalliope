from __future__ import absolute_import
from pushetta import Pushetta

from core.NeuronModule import NeuronModule, MissingParameterException


class Push_message(NeuronModule):
    """
    Neuron based on pushetta api. http://www.pushetta.com/
    """
    def __init__(self, **kwargs):
        """
        Send a push message to an android phone via Pushetta API
        :param message: Message to send
        :param api_key: The Pushetta service secret token
        :param channel_name: Pushetta channel name
        """
        super(Push_message, self).__init__(**kwargs)

        self.message = kwargs.get('message', None)
        self.api_key = kwargs.get('api_key', None)
        self.channel_name = kwargs.get('channel_name', None)

        # check if parameters have been provided
        if self._is_parameters_ok():
            p = Pushetta(self.api_key)
            p.pushMessage(self.channel_name, self.message)

    def _is_parameters_ok(self):
        """
        Check if received parameters are ok to perform operations in the neuron
        :return: true if parameters are ok, raise an exception otherwise

        .. raises:: NotImplementedError
        """
        if self.message is None:
            raise MissingParameterException("Pushetta neuron needs message to send")
        if self.api_key is None:
            raise MissingParameterException("Pushetta neuron needs api_key")
        if self.channel_name is None:
            raise MissingParameterException("Pushetta neuron needs channel_name")

        return True
