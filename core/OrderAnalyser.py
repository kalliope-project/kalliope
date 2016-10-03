import re

from core.Utils import Utils
from core.ConfigurationManager.BrainLoader import BrainLoader
from core.Models import Order
from core.NeuroneLauncher import NeuroneLauncher
import logging

logging.basicConfig()
logger = logging.getLogger("jarvis")


class OrderAnalyser:
    def __init__(self, order, main_controller=None, brain_file=None):
        """
        Class used to load brain and run neuron attached to the received order
        :param order: spelt order
        :param main_controller
        :param brain_file: To override the default brain.yml file
        """
        self.main_controller = main_controller
        self.order = order
        if brain_file is None:
            self.brain = BrainLoader.get_brain()
        else:
            self.brain = BrainLoader.get_brain(file_path=brain_file)
            logger.debug("Receiver order: %s" % self.order)

    def start(self):
        synapses_found = False
        for synapse in self.brain.synapses:
            for signal in synapse.signals:
                if type(signal) == Order:
                    if self._spelt_order_match_brain_order(signal.sentence):
                        synapses_found = True
                        logger.debug("Order found! Run neurons: %s" % synapse.neurons)
                        Utils.print_success("Order matched in the brain. Running synapse \"%s\"" % synapse.name)
                        for neuron in synapse.neurons:
                            NeuroneLauncher.start_neurone(neuron)

        if not synapses_found:
            Utils.print_info("No synapse match the captured order: %s" % self.order)

    def _spelt_order_match_brain_order(self, order_to_test):
        """
        test if the current order match the order spelt by the user
        :param order_to_test:
        :return:
        """
        my_regex = r"\b(?=\w)" + re.escape(order_to_test) + r"\b(?!\w)"

        if re.search(my_regex, self.order, re.IGNORECASE):
            return True
        return False


