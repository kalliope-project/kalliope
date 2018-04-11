import logging

from kalliope import SignalLauncher
from kalliope.core.NeuronModule import NeuronModule
from kalliope.core.ConfigurationManager.SettingEditor import SettingEditor

logging.basicConfig()
logger = logging.getLogger("kalliope")


class Deaf(NeuronModule):

    def __init__(self, **kwargs):
        super(Deaf, self).__init__(**kwargs)

        self.status = kwargs.get('status', None)

        # check if parameters have been provided
        if self._is_parameters_ok():
            signal_order = SignalLauncher.get_order_instance()
            if signal_order is not None:
                SettingEditor.set_deaf_status(signal_order.trigger_instance, self.status)

    def _is_parameters_ok(self):
        """
        Check if received parameters are ok to perform operations in the neuron
        :return: true if parameters are ok, raise an exception otherwise

        .. raises:: MissingParameterException
        """
        if self.status is None:
            logger.debug("[Deaf] You must specify a status with a boolean")
            return False
        return True
