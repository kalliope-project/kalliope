# coding: utf8
import re
from collections import Counter

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
        if isinstance(self.order, str):
            self.order = order.decode('utf-8')
        if brain_file is None:
            self.brain = BrainLoader.get_brain()
        else:
            self.brain = BrainLoader.get_brain(file_path=brain_file)
        logger.debug("OrderAnalyser, Received order: %s" % self.order)

    def start(self):
        synapses_found = False
        problem_in_neuron_found = False
        for synapse in self.brain.synapses:
            for signal in synapse.signals:
                if type(signal) == Order:
                    if self._spelt_order_match_brain_order_via_table(signal.sentence, self.order):
                        synapses_found = True
                        logger.debug("Order found! Run neurons: %s" % synapse.neurons)
                        Utils.print_success("Order matched in the brain. Running synapse \"%s\"" % synapse.name)
                        # if the order contains bracket, we get parameters said by the user
                        params = None
                        if self._is_containing_bracket(signal.sentence):
                            params = self._associate_order_params_to_values(signal.sentence)
                            logger.debug("Parameters for order: %s" % params)

                        for neuron in synapse.neurons:
                            if isinstance(neuron.parameters, dict):
                                print neuron.parameters
                                if "args" in neuron.parameters:
                                    logger.debug("The neuron wait for parameter")
                                    # check that the user added parameters to his order
                                    if params is None:
                                        # we don't raise an error and break the program but we don't run the neuron
                                        problem_in_neuron_found = True
                                        Utils.print_danger("Error: The neuron %s is waiting for argument. "
                                                           "Argument found in bracket in the given order" % neuron.name)
                                    else:
                                        # we add wanted arguments the existing neuron parameter dict
                                        for arg in neuron.parameters["args"]:
                                            if arg in params:
                                                logger.debug("Parameter %s added to the current parameter "
                                                             "of the neuron: %s" % (arg, neuron.name))
                                                neuron.parameters[arg] = params[arg]
                                            else:
                                                # we don't raise an error and break the program but
                                                # we don't run the neuron
                                                problem_in_neuron_found = True
                                                Utils.print_danger("Error: Argument \"%s\" not found in the"
                                                                   " order" % arg)

                            # if no error detected, we run the neuron
                            if not problem_in_neuron_found:
                                NeuroneLauncher.start_neurone(neuron)
                            else:
                                Utils.print_danger("A problem has been found in the Synapse.")


        if not synapses_found:
            Utils.print_info("No synapse match the captured order: %s" % self.order)

    def _associate_order_params_to_values(self, order_to_check):
        """
        Associate the variables from the order to the incoming user order
        :param order_to_check: the order to check
        :return: the dict corresponding to the key / value of the params
        """
        pattern = '\s+(?=[^\{\{\}\}]*\}\})'
        # Remove white spaces (if any) between the variable and the double brace then split
        list_word_in_order = re.sub(pattern, '', order_to_check).split()

        # get the order, defined by the first words before {{
        # /!\ Could be empty if order starts with double brace
        the_order = order_to_check[:order_to_check.find('{{')]

        # remove sentence before order which are sentences not matching anyway
        truncate_user_sentence = self.order[self.order.find(the_order):]
        truncate_list_word_said = truncate_user_sentence.split()

        # make dict var:value
        dict_var = {}
        for idx, ow in enumerate(list_word_in_order):
            if self._is_containing_bracket(ow):
                # remove bracket and grab the next value / stop value
                var_name = ow.replace("{{", "").replace("}}", "")
                stop_value = self._get_next_value_list(list_word_in_order[idx:])
                if stop_value is None:
                    dict_var[var_name] = " ".join(truncate_list_word_said)
                    break
                for word_said in truncate_list_word_said:
                    if word_said == stop_value:
                        break
                    if var_name in dict_var:
                        dict_var[var_name] += " " + word_said
                        truncate_list_word_said = truncate_list_word_said[1:]
                    else:
                        dict_var[var_name] = word_said
            truncate_list_word_said = truncate_list_word_said[1:]
        return dict_var

    @staticmethod
    def _is_containing_bracket(sentence):
        # print "sentence to test %s" % sentence
        pattern = r"{{|}}"
        # prog = re.compile(pattern)
        check_bool = re.search(pattern, sentence)
        if check_bool is not None:
            return True
        return False

    @staticmethod
    def _get_next_value_list(list_to_check):
        ite = list_to_check.__iter__()
        next(ite, None)
        return next(ite, None)

    def _spelt_order_match_brain_order_via_table(self, order_to_analyse, user_said):
        """
        return true if all string that are in the sentence are present in the order to test
        :param order_to_analyse: String order to test
        :param user_said: String to compare to the order
        :return: True if all string are present in the order
        """
        list_word_user_said = user_said.split()
        split_order_without_bracket = self._get_split_order_without_bracket(order_to_analyse)

        # if all words in the list of what the user said in in the list of word in the order
        return self._counter_subset(split_order_without_bracket, list_word_user_said)

    @staticmethod
    def _get_split_order_without_bracket(order):
        """
        Get an order with bracket inside like: "hello my name is {{ name }}.
        return a list of string without bracket like ["hello", "my", "name", "is"]
        :param order: sentence to split
        :return: list of string without bracket
        """
        pattern = r"((?:{{\s*)[\w\.]+(?:\s*}}))"
        # find everything like {{ word }}
        matches = re.findall(pattern, order)
        for match in matches:
            order = order.replace(match, "")
        # then split
        split_order = order.split()
        return split_order

    @staticmethod
    def _counter_subset(list1, list2):
        """
        check if the number of occurrences matches
        :param list1:
        :param list2:
        :return:
        """
        c1, c2 = Counter(list1), Counter(list2)
        for k, n in c1.items():
            if n > c2[k]:
                return False
        return True
