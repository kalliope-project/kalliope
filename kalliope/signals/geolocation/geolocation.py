import logging
from threading import Thread

from kalliope.core import SignalModule

logging.basicConfig()
logger = logging.getLogger("kalliope")


class Geolocation(SignalModule, Thread):
    def __init__(self, **kwargs):
        super(Geolocation, self).__init__(**kwargs)

    def run(self):
        logger.debug("[Geolocalisation] Loading ...")
        self.list_synapses_with_geolocalion = list(super(Geolocation, self).get_list_synapse())

    @staticmethod
    def check_parameters(parameters):
        """
        Overwritten method
        receive a dict of parameter from a geolocation signal and them
        :param parameters: dict of parameters
        :return: True if parameters are valid
        """
        # check mandatory parameters
        mandatory_parameters = ["latitude", "longitude", "radius"]
        return all(key in parameters for key in mandatory_parameters)
