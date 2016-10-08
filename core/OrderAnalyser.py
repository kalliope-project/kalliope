import re

from core.Utils import Utils
from core.ConfigurationManager.BrainLoader import BrainLoader
from core.Models import Order
from core.NeuroneLauncher import NeuroneLauncher
from Cosine import *

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
                        params = {}
                        if self._is_containing_bracket(signal.sentence):
                            params = self._associate_order_params_to_values(signal.sentence)
                        for neuron in synapse.neurons:
                            NeuroneLauncher.start_neurone(neuron, params)

        if not synapses_found:
            Utils.print_info("No synapse match the captured order: %s" % self.order)

    def _spelt_order_match_brain_order(self, order_to_test):
        """

        test if the current order match the order spelt by the user
        :param order_to_test:
        :return:
        """
        # TODO : In "order_to_test" should we remove double brace and variable name before checking to optimise the cosine ?
        user_vector = text_to_vector(self.order)
        order_vector = text_to_vector(order_to_test)

        cosine = get_cosine(user_vector, order_vector)
        logger.debug("the cosine : %s, pour user_vector: %s , order_vector: %s" % (cosine, self.order, order_to_test))
        return cosine >= 0.5


    def _associate_order_params_to_values(self, order_to_check):
        """
        Associate the variables from the order to the incoming user order
        :param order: the order to check
        :return: the dict corresponding to the key / value of the params
        """

        # Remove white spaces (if any) between the variable and the double brace then split
        list_word_in_order = re.sub('\s+(?=[^\{\{\}\}]*\}\})', '', order_to_check).split()

        # get the order, defined by the first words before {{
        # /!\ Could be empty if order starts with double brace
        the_order = order_to_check[:order_to_check.find('{{')]

        # remove sentence before order which are sentences not matching anyway
        truncate_user_sentence = self.order[self.order.find(the_order):]
        truncate_list_word_said = truncate_user_sentence.split()

        # make dict var:value
        dictVar = {}
        for idx, ow in enumerate(list_word_in_order):
            if self._is_containing_bracket(ow):
                # remove bracket and grab the next value / stop value
                varname = ow.replace("{{", "").replace("}}", "")
                stopValue = self._get_next_value_list(list_word_in_order[idx:])
                if stopValue is None:
                    dictVar[varname] = " ".join(truncate_list_word_said)
                    break
                for word_said in truncate_list_word_said:
                    if word_said == stopValue: break
                    if varname in dictVar:
                        dictVar[varname] += " " + word_said
                        truncate_list_word_said = truncate_list_word_said[1:]
                    else:
                        dictVar[varname] = word_said
            truncate_list_word_said = truncate_list_word_said[1:]
        return dictVar


    @staticmethod
    def _is_containing_bracket(sentence):
        # print "sentence to test %s" % sentence
        pattern = r"{{|}}"
        # prog = re.compile(pattern)
        bool = re.search(pattern, sentence)
        if bool is not None:
            return True
        return False

    @staticmethod
    def _get_next_value_list(list):
        ite = list.__iter__()
        next(ite, None)
        return next(ite, None)

