import logging

from kalliope.core.Utils import Utils

logging.basicConfig()
logger = logging.getLogger("kalliope")


class NeuroneLauncher:

    def __init__(self):
        pass

    @classmethod
    def start_neurone(cls, neuron):
        """
        Start a neuron plugin
        :param neuron: neuron object
        :type neuron: Neuron
        :return:
        """
        logger.debug("Run plugin \"%s\" with parameters %s" % (neuron.name, neuron.parameters))
        return Utils.get_dynamic_class_instantiation("neurons", neuron.name.capitalize(), neuron.parameters)
