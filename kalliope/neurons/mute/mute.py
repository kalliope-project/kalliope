import logging

from kalliope import SignalLauncher
from kalliope.core.NeuronModule import NeuronModule, MissingParameterException
from kalliope.signals.order import Order

logging.basicConfig()
logger = logging.getLogger("kalliope")


class Mute(NeuronModule):

    def __init__(self, **kwargs):
        super(Mute, self).__init__(**kwargs)

        self.status = kwargs.get('status', None)

        # check if parameters have been provided
        if self._is_parameters_ok():
            for signal in SignalLauncher.get_launched_signals_list():
                if isinstance(signal, Order):
                    signal.set_mute_status(self.status)

    def _is_parameters_ok(self):
        """
        Check if received parameters are ok to perform operations in the neuron
        :return: true if parameters are ok, raise an exception otherwise

        .. raises:: MissingParameterException
        """
        if self.status is None:
            logger.debug("[Mute] You must specify a status with a boolean")
            return False
        return True
