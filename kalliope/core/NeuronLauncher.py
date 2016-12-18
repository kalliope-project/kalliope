import logging

from kalliope.core.Utils.Utils import Utils
from kalliope.core.ConfigurationManager.SettingLoader import SettingLoader

logging.basicConfig()
logger = logging.getLogger("kalliope")


class NeuronLauncher:

    def __init__(self):
        pass

    @classmethod
    def start_neuron(cls, neuron):
        """
        Start a neuron plugin
        :param neuron: neuron object
        :type neuron: Neuron
        :return:
        """
        logger.debug("Run plugin \"%s\" with parameters %s" % (neuron.name, neuron.parameters))
        sl = SettingLoader()
        settings = sl.settings
        neuron_folder = None
        if settings.resources:
            neuron_folder = settings.resources.neuron_folder
        return Utils.get_dynamic_class_instantiation(package_name="neurons",
                                                     module_name=neuron.name,
                                                     parameters=neuron.parameters,
                                                     resources_dir=neuron_folder)
