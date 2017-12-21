# coding: utf8
import collections
from collections import Counter
import six
from jinja2 import Template

from kalliope.core.NeuronParameterLoader import NeuronParameterLoader

from kalliope.core.Models.MatchedSynapse import MatchedSynapse
from kalliope.core.Utils.Utils import Utils
from kalliope.core.ConfigurationManager import SettingLoader

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
        if isinstance(order, six.binary_type):
            order = order.decode('utf-8')

        # We use a namedtuple to associate the synapse and the signal of the synapse
        synapse_order_tuple = collections.namedtuple('tuple_synapse_matchingOrder',
                                                     ['synapse', 'order'])

        list_match_synapse = list()

        # if the received order is None we can stop the process immediately
        if order is None:
            return list_match_synapse

        # test each synapse from the brain
        for synapse in cls.brain.synapses:
            for signal in synapse.signals:
                # we are only concerned by synapse with a order type of signal
                if signal.name == "order":
                    # get the type of matching expected, by default "normal"
                    expected_matching_type = "normal"
                    signal_order = None

                    if isinstance(signal.parameters, str):
                        signal_order = signal.parameters
                    if isinstance(signal.parameters, dict):
                        try:
                            signal_order = signal.parameters["text"]
                        except KeyError:
                            logger.debug("[OrderAnalyser] Warning, missing parameter 'text' in order. "
                                         "Order will be skipped")
                            continue
                        try:
                            expected_matching_type = signal.parameters["matching-type"]
                        except KeyError:
                            logger.debug("[OrderAnalyser] Warning, missing parameter 'matching-type' in order. "
                                         "Fallback to 'normal'")
                            expected_matching_type = "normal"

                    if cls.is_order_matching(user_order=order,
                                             signal_order=signal_order,
                                             expected_order_type=expected_matching_type):
                        # the order match the synapse, we add it to the returned list
                        logger.debug("Order found! Run synapse name: %s" % synapse.name)
                        Utils.print_success("Order matched in the brain. Running synapse \"%s\"" % synapse.name)
                        list_match_synapse.append(synapse_order_tuple(synapse=synapse, order=signal_order))

        # create a list of MatchedSynapse from the tuple list
        list_synapse_to_process = list()
        for tuple_el in list_match_synapse:
            new_matching_synapse = MatchedSynapse(matched_synapse=tuple_el.synapse,
                                                  matched_order=tuple_el.order,
                                                  user_order=order)
            list_synapse_to_process.append(new_matching_synapse)

        return list_synapse_to_process

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

    @classmethod
    def is_normal_matching(cls, user_order, signal_order):
        """
        True if :
            - all word in the user_order are present in the signal_order
        :param user_order: order from the user
        :param signal_order: order in the signal
        :return: Boolean
        """
        logger.debug("[OrderAnalyser] is_normal_matching called with user_order: %s, signal_order: %s" % (user_order,
                                                                                                          signal_order))
        split_user_order = user_order.split()
        split_signal_order_without_brackets = cls._get_split_order_without_bracket(signal_order)

        c1, c2 = Counter(split_signal_order_without_brackets), Counter(split_user_order)
        for k, n in c1.items():
            if n > c2[k]:
                return False
        return True

    @classmethod
    def is_strict_matching(cls, user_order, signal_order):
        """
        True if :
            - all word in the user_order are present in the signal_order
            - no additional word
        :param user_order: order from the user
        :param signal_order: order in the signal
        :return: Boolean
        """
        logger.debug("[OrderAnalyser] is_strict_matching called with user_order: %s, signal_order: %s" % (user_order,
                                                                                                          signal_order))
        if cls.is_normal_matching(user_order=user_order, signal_order=signal_order):

            # if the signal order contains bracket, we need to instantiate it with loaded parameters from the user order
            if Utils.is_containing_bracket(signal_order):
                signal_order = cls._get_instantiated_order_signal_from_user_order(signal_order, user_order)

            split_user_order = user_order.split()
            split_instantiated_signal = signal_order.split()

            if len(split_user_order) == len(split_instantiated_signal):
                return True

        return False

    @classmethod
    def is_ordered_strict_matching(cls, user_order, signal_order):
        """
       True if :
            - all word in the user_order are present in the signal_order
            - no additional word
            - same order as word present in signal_order
        :param user_order: order from the user
        :param signal_order: order in the signal
        :return: Boolean
        """
        logger.debug(
            "[OrderAnalyser] ordered_strict_matching called with user_order: %s, signal_order: %s" % (user_order,
                                                                                                      signal_order))
        if cls.is_normal_matching(user_order=user_order, signal_order=signal_order) and \
                cls.is_strict_matching(user_order=user_order, signal_order=signal_order):
            # if the signal order contains bracket, we need to instantiate it with loaded parameters from the user order
            if Utils.is_containing_bracket(signal_order):
                signal_order = cls._get_instantiated_order_signal_from_user_order(signal_order, user_order)

            split_user_order = user_order.split()
            split_signal_order = signal_order.split()
            return split_user_order == split_signal_order

        return False

    @classmethod
    def is_order_matching(cls, user_order, signal_order, expected_order_type="normal"):
        """
        return True if the user_order match the signal_order following the expected_order_type
        where "expected_order_type" is in
        - normal: normal matching. all words are present in the user_order. this is the default
        - strict: only word in the user order match. no more word
        - ordered-strict: only word in the user order and in the same order
        :param user_order: order from the user
        :param signal_order: order in the signal
        :param expected_order_type: type of order (normal, strict, ordered-strict)
        :return: True if the order match
        """
        matching_type_function = {
            "normal": cls.is_normal_matching,
            "strict": cls.is_strict_matching,
            "ordered-strict": cls.is_ordered_strict_matching
        }

        # Lowercase all incoming
        user_order = user_order.lower()
        signal_order = signal_order.lower()

        if expected_order_type in matching_type_function:
            return matching_type_function[expected_order_type](user_order, signal_order)
        else:
            logger.debug("[OrderAnalyser] non existing matching-type: '%s', fallback to 'normal'" % expected_order_type)
            return matching_type_function["normal"](user_order, signal_order)

    @classmethod
    def _get_instantiated_order_signal_from_user_order(cls, signal_order, user_order):
        """
        return instantiated signal order with parameters loaded from the user order
        E.g:
        signal_order = "this is an {{ variable }}
        user_order = "this is an order"

        returned value is: "this is an order"

        :param user_order: the order from the user
        :param signal_order: the order with brackets from the synapse
        :return: jinja instantiated order from the signal
        """
        # get parameters
        parameters_from_user_order = NeuronParameterLoader.get_parameters(synapse_order=signal_order,
                                                                          user_order=user_order)
        # we load variables into the expected order from the signal
        t = Template(signal_order)
        signal_order = t.render(**parameters_from_user_order)

        return signal_order
