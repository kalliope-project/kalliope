import logging
from abc import ABCMeta, abstractmethod
from kalliope.core import Utils

from kalliope.core.ConfigurationManager import BrainLoader

logging.basicConfig()
logger = logging.getLogger("kalliope")


class MissingParameter(Exception):
    """
    A geolocation must contain latitude, longitude, radius.

    .. seealso:: Geolocation
    """
    pass


class SignalModule(object):
    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        super(SignalModule, self).__init__(**kwargs)
        # get the child who called the class
        self.signal_name = self.__class__.__name__

        Utils.print_info('Init Signal :' + self.signal_name)
        self.brain = BrainLoader().brain

    def get_list_synapse(self):
        for synapse in self.brain.synapses:
            for signal in synapse.signals:
                # if the signal is a child we add it to the synapses list
                if signal.name == self.signal_name.lower(): # Lowercase !
                    if not self.check_parameters(parameters=signal.parameters):
                        logger.debug(
                            "[SignalModule] The signal " + self.signal_name + " is missing mandatory parameters, check documentation")
                        raise MissingParameter()
                    else:
                        yield synapse

    @staticmethod
    @abstractmethod
    def check_parameters(parameters):
        raise NotImplementedError("[SignalModule] Must override check_parameters method !")
