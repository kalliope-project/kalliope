# coding: utf8
import collections
from collections import Counter

from kalliope.core.Utils.Utils import Utils
from kalliope.core.ConfigurationManager import SettingLoader
from kalliope.core.Models import Order

import logging

logging.basicConfig()
logger = logging.getLogger("kalliope")


class OrderAnalyser:
    """
    This Class is used to get a list of synapses that match a given Spoken order
    """

    brain = None
    settings = None

    @classmethod
    def __init__(cls):
        cls.settings = SettingLoader().settings

    @classmethod
    def get_matching_synapse(cls, order, brain=None):
        """
        Return the list of matching synapses from the given order
        :param order: The user order
        :param brain: The loaded brain
        :return: The List of synapses matching the given order
        """
        cls.brain = brain
        logger.debug("[OrderAnalyser] Received order: %s" % order)
        if isinstance(order, str):
            order = order.decode('utf-8')

        # We use a namedtuple to associate the synapse and the signal of the synapse
        synapse_order_tuple = collections.namedtuple('tuple_synapse_matchingOrder',
                                                     ['synapse', 'order'])

        list_match_synapse = list()

        # test each synapse from the brain
        for synapse in cls.brain.synapses:
            # we are only concerned by synapse with a order type of signal
            for signal in synapse.signals:
                if type(signal) == Order:
                    if cls.spelt_order_match_brain_order_via_table(signal.sentence, order):
                        # the order match the synapse, we add it to the returned list
                        logger.debug("Order found! Run synapse name: %s" % synapse.name)
                        Utils.print_success("Order matched in the brain. Running synapse \"%s\"" % synapse.name)
                        list_match_synapse.append(synapse_order_tuple(synapse=synapse, order=signal.sentence))
        return list_match_synapse

    @classmethod
    def spelt_order_match_brain_order_via_table(cls, order_to_analyse, user_said):
        """
        return true if all formatted(_format_sentences_to_analyse(order_to_analyse, user_said)) strings
                that are in the sentence are present in the order to test.
        :param order_to_analyse: String order to test
        :param user_said: String to compare to the order
        :return: True if all string are present in the order
        """
        # Lowercase all incoming
        order_to_analyse = order_to_analyse.lower()
        user_said = user_said.lower()

        logger.debug("[spelt_order_match_brain_order_via_table] "
                     "order to analyse: %s, "
                     "user sentence: %s"
                     % (order_to_analyse, user_said))

        list_word_user_said = user_said.split()
        split_order_without_bracket = cls._get_split_order_without_bracket(order_to_analyse)

        # if all words in the list of what the user said in in the list of word in the order
        return cls._counter_subset(split_order_without_bracket, list_word_user_said)

    @staticmethod
    def _get_split_order_without_bracket(order):
        """
        Get an order with bracket inside like: "hello my name is {{ name }}.
        return a list of string without bracket like ["hello", "my", "name", "is"]
        :param order: sentence to split
        :return: list of string without bracket
        """

        matches = Utils.find_all_matching_brackets(order)
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
