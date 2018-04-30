import logging

from kalliope.core import NeuronModule
from kalliope.core.NeuronModule import MissingParameterException, InvalidParameterException
from kalliope.core.NotificationManager import NotificationManager

logging.basicConfig()
logger = logging.getLogger("kalliope")


class Signals(NeuronModule):
    def __init__(self, **kwargs):
        super(Signals, self).__init__(**kwargs)

        # get the command
        self.notification = kwargs.get('notification', False)
        self.payload = kwargs.get('payload', False)

        if self._is_parameters_ok():

            logger.debug("[Signals] Send a notification to all subscribed classes, notification: '%s', payload: %s"
                         % (self.notification, self.payload))

            NotificationManager.send_notification(self.notification, self.payload)

    def _is_parameters_ok(self):

        if self.notification is None:
            raise MissingParameterException("[Signals] This neuron require a 'notification parameter'")

        return True

    @staticmethod
    def str_to_bool(s):
        if s in ['True', 'true', '1']:
            return True
        elif s in ['False', 'false', '0']:
            return False
        else:
            return False
