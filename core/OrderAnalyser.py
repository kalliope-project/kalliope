import re

from core import ConfigurationManager
from core.ConfigurationManager.BrainLoader import BrainLoader
from core.NeuroneLauncher import NeuroneLauncher
import logging


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
            self.brain = ConfigurationManager.get_brain()
        else:
            self.brain = BrainLoader(brain_file).get_config()
        logging.info("Receiver order: %s" % self.order)

    def start(self):
        for el in self.brain:
            whens = el["when"]
            for when in whens:
                brain_order = when["order"]
                # print "order to test: %s" % brain_order
                if self._spelt_order_match_brain_order(brain_order):
                    print "Order found! Run neurons: %s" % el["neurons"]
                    neurons = el["neurons"]
                    for neuron in neurons:
                        NeuroneLauncher.start_neurone(neuron)

        # once we ran all plugin, we can start back jarvis trigger
        if self.main_controller is not None:
            self.main_controller.unpause_jarvis_trigger()

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


