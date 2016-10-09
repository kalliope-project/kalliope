from __future__ import absolute_import
from pushetta import Pushetta

from core.NeuronModule import NeuronModule


class Push_message(NeuronModule):
    """
    Neuron based on pushetta api. http://www.pushetta.com/
    """

    def __init__(self, message=None, api_key=None, channel_name=None, **kwargs):
        """
        Send a push message to an android phone via Pushetta API
        :param message: Message to send
        :param api_key: The Pushetta service secret token
        :param channel_name: Pushetta channel name
        :return:
        """
        super(Push_message, self).__init__(**kwargs)
        if message is None:
            raise NotImplementedError("Pushetta neuron needs message to send")

        if api_key is None:
            raise NotImplementedError("Pushetta neuron needs api_key")
        if channel_name is None:
            raise NotImplementedError("Pushetta neuron needs channel_name")

        p = Pushetta(api_key)
        p.pushMessage(channel_name, message)
