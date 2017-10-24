import logging
from threading import Thread

from kalliope.core import Utils
from kalliope.core.ConfigurationManager import BrainLoader

logging.basicConfig()
logger = logging.getLogger("kalliope")


class Geolocation(Thread):

    def __init__(self):
        super(Geolocation, self).__init__()
        Utils.print_info('Init Geolocation')
        self.brain = BrainLoader().get_brain()

    def run(self):
        logger.debug("[Geolocalisation] Loading ...")
        self.list_synapses_with_geolocalion = self._get_list_synapse_with_geolocation(self.brain)

    @classmethod
    def _get_list_synapse_with_geolocation(cls, brain):
        """
        return the list of synapse that use geolocation as signal in the provided brain
        :param brain: Brain object that contain all synapses loaded
        :type brain: Brain
        :return: list of synapse that use geolocation as signal
        """
        for synapse in brain.synapses:
            for signal in synapse.signals:
                # if the signal is an event we add it to the task list
                if signal.name == "geolocation":
                    if not cls._check_geolocation(signal.parameters):
                        logger.debug("[Geolocation] The signal is missing mandatory parameters, check documentation")
                    else:
                        yield synapse

    @staticmethod
    def _check_geolocation(parameters):
        """
        receive a dict of parameter from a geolocation signal and them
        :param parameters: dict of parameters
        :return: True if parameters are valid
        """
        # check mandatory parameters
        mandatory_parameters = ["latitude", "longitude", "radius"]
        return all(key in parameters for key in mandatory_parameters)