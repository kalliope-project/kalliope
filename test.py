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

user_said = "regle le reveil pour sept heures et dix minutes"
order = "regle le reveil pour {{ hour }} heures et {{ minute }} minutes"


brain = BrainLoader.get_brain()
# take a look to each order


def _is_containing_bracket(sentence):
    # print "sentence to test %s" % sentence
    pattern = r"{{|}}"
    # prog = re.compile(pattern)
    bool = re.search(pattern, sentence)
    if bool is not None:
        return True
    return False

list_word = user_said.split()
# list_word = ["je", "voudrais"]
print "user said: %s" % list_word


def _get_order_without_variables(list_word_in_order):

   pass


# check if the order contain bracket
if _is_containing_bracket(order):
    # get a table of word said
    list_word_in_order = order.split()
    print "order matched: %s" % list_word_in_order
    split_orider_variable = _get_order_without_variables(list_word_in_order)


# return the beginning of the sentence before first bracket
# return sentence[:sentence.find('{{')]

# split each word
# 









