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
    list_parameter_position_and_name = list()

    index = 0   # index to count element in the list counting the brackets
    returned_index = 1  # this is the index where the parameter is placed
    for el in list_word_in_order:
        if _is_containing_opening_bracket(el):
            new_parameter = dict()
            new_parameter["name"] = list_word_in_order[index+1]
            new_parameter["index"] = returned_index
            list_parameter_position_and_name.append(new_parameter)
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
    print list_parameter_position_and_name
    returned_dict = dict()
    returned_dict["list_word_without_bracket"] = list_word_without_bracket
    returned_dict["list_parameter_position_and_name"] = list_parameter_position_and_name
    return returned_dict


def _get_usefull_words(list_word_user_said, list_word_without_bracket):
    first_valid_word = list_word_without_bracket[0]
    last_word_valid_word = list_word_without_bracket[len(list_word_without_bracket)-1]
    print first_valid_word
    print last_word_valid_word

    start_index = list_word_user_said.index(first_valid_word)
    stop_index = list_word_user_said.index(last_word_valid_word)

    new_list = list()
    for x in (range(start_index, stop_index)):
        new_list.append(list_word_user_said[int(x)])
    print new_list

    return new_list


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
    parameters_position_and_name = returned_dict["list_parameter_position_and_name"]

    number_of_word_in_order = len(list_word_without_bracket)
    # if all words in the list of what the user said in in the list of word in the order
    if len(set(list_word_without_bracket).intersection(list_word_user_said)) == number_of_word_in_order:
        # we match the order!
        print "order matched !"     # we can get parameters in the sentence the user said

        # remove unused word in the list of word spelt by the user.
        usefull_words_in_user_said_list = _get_usefull_words(list_word_user_said, list_word_without_bracket)
        val_parameter = dict()
        for el in parameters_position_and_name:
            print el["name"]
            print
            val_parameter[el["name"]] = list_word_user_said[int(el["index"])]

        print "The dict Var : %s" % val_parameter


# make a list of word
list_word_user_said = user_said.split()
print "user said: %s" % list_word_user_said

# check if the order contain bracket
if _is_containing_bracket(order):
    print "The order contain bracket"
    # create a list from the order to test
    list_word_in_order = order.split()
    try_match_order_in_synapse(list_word_user_said, list_word_in_order)












