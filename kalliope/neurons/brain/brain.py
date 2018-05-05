import logging

from kalliope import Utils, BrainLoader
from kalliope.core import NeuronModule
from kalliope.core.NeuronModule import MissingParameterException

logging.basicConfig()
logger = logging.getLogger("kalliope")


class Brain(NeuronModule):

    def __init__(self, **kwargs):
        super(Brain, self).__init__(**kwargs)

        self.synapse_name = kwargs.get('synapse_name', None)
        self.enabled = kwargs.get('enabled', None)

        new_status = "unknown"
        if self._is_parameters_ok():
            brain = BrainLoader().brain
            if self.enabled:
                if brain.enable_synapse_by_name(self.synapse_name):
                    new_status = "enabled"
            else:
                if brain.disable_synapse_by_name(self.synapse_name):
                    new_status = "disabled"

        message = {
            "synapse_name": self.synapse_name,
            "status": new_status
        }
        self.say(message)

    def _is_parameters_ok(self):
        """
        Check if received parameters are ok to perform operations in the neuron
        :return: true if parameters are ok, raise an exception otherwise

        .. raises:: MissingParameterException
        """
        if self.synapse_name is None:
            raise MissingParameterException("[Brain neuron] You must specify a 'synapse_name'")
        if self.enabled is None:
            raise MissingParameterException("[Brain neuron] You must specify a 'enabled boolean'")

        self.enabled = Utils.str_to_bool(self.enabled)

        return True
