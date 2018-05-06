# coding: utf8
import collections
from collections import Counter
import six
import yaml
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

        # if the received order is None we can stop the process immediately
        if order is None:
            return list()

        # test each synapse from the brain
        list_match_synapse = cls.get_list_match_synapse(order, synapse_order_tuple)

        # create a list of MatchedSynapse from the tuple list
        list_synapse_to_process = cls.get_list_synapses_to_process(list_match_synapse, order)

        return list_synapse_to_process

    @classmethod
    def get_list_synapses_to_process(cls, list_match_synapse, order):
        list_synapse_to_process = list()
        for tuple_el in list_match_synapse:
            new_matching_synapse = MatchedSynapse(matched_synapse=tuple_el.synapse,
                                                  matched_order=tuple_el.order,
                                                  user_order=order)
            list_synapse_to_process.append(new_matching_synapse)
        return list_synapse_to_process

    @classmethod
    def get_list_match_synapse(cls, order, synapse_order_tuple):
        list_match_synapse = list()
        for synapse in cls.brain.synapses:
            if synapse.enabled:
                for signal in synapse.signals:
                    # we are only concerned by synapse with a order type of signal
                    if signal.name == "order":
                        # get the type of matching expected, by default "normal"
                        expected_matching_type = "normal"
                        signal_order = None

                        if isinstance(signal.parameters, str) or isinstance(signal.parameters, six.text_type):
                            signal_order = signal.parameters
                        if isinstance(signal.parameters, dict):
                            try:
                                signal_order = signal.parameters["text"]
                            except KeyError:
                                logger.debug("[OrderAnalyser] Warning, missing parameter 'text' in order. "
                                             "Order will be skipped")
                                continue

                            expected_matching_type = cls.get_matching_type(signal)

                            order = cls.order_correction(order, signal)

                        if cls.is_order_matching(user_order=order,
                                                 signal_order=signal_order,
                                                 expected_order_type=expected_matching_type):
                            # the order match the synapse, we add it to the returned list
                            logger.debug("Order found! Run synapse name: %s" % synapse.name)
                            Utils.print_success("Order matched in the brain. Running synapse \"%s\"" % synapse.name)
                            list_match_synapse.append(synapse_order_tuple(synapse=synapse, order=signal_order))
        return list_match_synapse

    @classmethod
    def order_correction(cls, order, signal):

        stt_correction_list = list()

        stt_correction_file_path = cls.get_stt_correction_file_path(signal)
        stt_correction = cls.get_stt_correction(signal)

        if stt_correction_file_path is not None:
            stt_correction_list = cls.load_stt_correction_file(stt_correction_file_path)
        if stt_correction is not None:
            stt_correction_list = cls.override_stt_correction_list(stt_correction_list, stt_correction)
        if stt_correction_list:
            order = cls.override_order_with_correction(order, stt_correction_list)
        return order

    @staticmethod
    def get_stt_correction(signal):
        stt_correction = None
        try:
            stt_correction = signal.parameters["stt-correction"]
            logger.debug("[OrderAnalyser] stt-correction provided by user")
        except KeyError:
            logger.debug("[OrderAnalyser] No stt-correction provided")
        return stt_correction

    @staticmethod
    def get_stt_correction_file_path(signal):
        stt_correction_file_path = None
        try:
            stt_correction_file_path = signal.parameters["stt-correction-file"]
            logger.debug("[OrderAnalyser] stt-correction-file provided by user")
        except KeyError:
            logger.debug("[OrderAnalyser] No stt-correction-file provided")
        return stt_correction_file_path

    @staticmethod
    def get_matching_type(signal):
        expected_matching_type = "normal"
        try:
            expected_matching_type = signal.parameters["matching-type"]
        except KeyError:
            logger.debug("[OrderAnalyser] Warning, missing parameter 'matching-type' in order. "
                         "Fallback to 'normal'")
        return expected_matching_type

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
        return True if the user_order matches the signal_order following the expected_order_type
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

    @classmethod
    def override_order_with_correction(cls, order, stt_correction):
        logger.debug("[OrderAnalyser] override_order_this_correction: stt_correction list: %s" % stt_correction)
        logger.debug("[OrderAnalyser] override_order_this_correction: order before correction: %s" % order)
        for correction in stt_correction:
            try:
                input_val = str(correction["input"])
                output_val = str(correction["output"])
            except KeyError as e:
                logger.debug("[OrderAnalyser] override_order_this_correction: "
                             "Missing key %s. Order will not be modified" % e)
                return order

            if str(input_val) in order.split():
                logger.debug("[OrderAnalyser] STT override '%s' by '%s'" % (input_val, output_val))
                order = order.replace(input_val, output_val)

        return order

    @classmethod
    def load_stt_correction_file(cls, stt_correction_file):
        stt_correction_file_path = Utils.get_real_file_path(stt_correction_file)
        stt_correction_file = open(stt_correction_file_path, "r")
        stt_correction = yaml.load(stt_correction_file)

        return stt_correction

    @classmethod
    def override_stt_correction_list(cls, stt_correction_list_to_override, correction_list):
        # add non existing dict
        for correction_to_check in correction_list:
            if correction_to_check["input"] not in (x["input"] for x in stt_correction_list_to_override):
                stt_correction_list_to_override.append(correction_to_check)

        # override dict with same input
        for correction_to_override in stt_correction_list_to_override:
            for correction_to_check in correction_list:
                if correction_to_check["input"] == correction_to_override["input"]:
                    correction_to_override["output"] = correction_to_check["output"]
                    break

        return stt_correction_list_to_override
