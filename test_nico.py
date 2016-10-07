# -*- coding: utf-8 -*-
import os

import re

from core.ConfigurationManager import SettingLoader
from core.ConfigurationManager.BrainLoader import BrainLoader
from core.CrontabManager import CrontabManager
from core.Models import Order
from core.OrderAnalyser import OrderAnalyser

import logging

from core.TriggerLauncher import TriggerLauncher


# user_said = "maman je voudrais ecouter ACDC"
# order = "je voudrais ecouter {{ artist_name }}"

user_said = "jarvis regle le reveil pour sept heures et dix minutes please"
order = "regle le reveil pour {{ hour }} heures et {{ minute }} minutes"


def _is_containing_closing_bracket(sentence):
    pattern = r"}}"
    bool = re.search(pattern, sentence)
    if bool is not None:
        return True
    return False


def _is_containing_opening_bracket(sentence):
    pattern = r"{{"
    bool = re.search(pattern, sentence)
    if bool is not None:
        return True
    return False


def _is_containing_bracket(sentence):
    pattern = r"{{|}}"
    bool = re.search(pattern, sentence)
    if bool is not None:
        return True
    return False


def _get_list_word_in_order_without_parameter(list_word_in_order):
    """
    Receive a list of word with bracket like
    ['regle', 'le', 'reveil', 'pour', '{{', 'hour', '}}', 'heures', 'et', '{{', 'minute', '}}', 'minutes']
    Return a dict without parameter and a list of parameter place:

    TODO insert example
    :param list_word_in_order: List of string that can contain a word or brackets
    :return: Dict
    """
    print list_word_in_order
    list_word_without_bracket = list()
    list_parameter_position = list()

    index = 0   # index to count element in the list counting the brackets
    returned_index = 0  # this is the index where the parameter is placed
    for el in list_word_in_order:
        if _is_containing_opening_bracket(el):
            list_parameter_position.append(returned_index)
        else:
            try:
                # if the next element is not a closing bracket
                if not _is_containing_closing_bracket(list_word_in_order[index+1]) and not \
                        _is_containing_closing_bracket(el):
                    # so we are not facing a parameter. we can add the word to the list
                    list_word_without_bracket.append(el)
                else:
                    returned_index -= 1
            except IndexError:
                if not _is_containing_bracket(el):
                    list_word_without_bracket.append(el)
        returned_index += 1
        index += 1

    print list_word_without_bracket
    print list_parameter_position
    returned_dict = dict()
    returned_dict["list_word_without_bracket"] = list_word_without_bracket
    returned_dict["list_parameter_position"] = list_parameter_position
    return returned_dict


def try_match_order_in_synapse(list_word_user_said, list_word_in_order):
    """
    Test if what the user said match an order with brackets
    :param list_word_user_said: List of words that the user said
    :param list_word_in_order: List of word in the order to test, including bracket
    :return: True if the order match
    """
    # first, get a list of word that composed to order without variable
    returned_dict = _get_list_word_in_order_without_parameter(list_word_in_order)

    list_word_without_bracket = returned_dict["list_word_without_bracket"]
    parameters_position = returned_dict["list_parameter_position"]

    number_of_word_in_order = len(list_word_without_bracket)
    # if all words in the list of what the user said in in the list of word in the order
    if len(set(list_word_without_bracket).intersection(list_word_user_said)) == number_of_word_in_order:
        # we match the order!
        print "order matched !"
        # we can get parameters in the sentence the user said
        # TODO get parameters
        # # we create a new list from the order with parameter tag inside
        # order_list_with_parameter_tag = None
        # for position in parameters_position:
        #     order_list_with_parameter_tag = list_word_without_bracket.insert(int(position), "#PARAMETER#")
        # print order_list_with_parameter_tag


# make a list of word
list_word_user_said = user_said.split()
print "user said: %s" % list_word_user_said

# check if the order contain bracket
if _is_containing_bracket(order):
    print "The order contain bracket"
    # create a list from the order to test
    list_word_in_order = order.split()
    try_match_order_in_synapse(list_word_user_said, list_word_in_order)












