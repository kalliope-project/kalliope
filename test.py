# coding: utf8
import logging
import re
from collections import Counter

from core import OrderAnalyser
logging.basicConfig()
logger = logging.getLogger("jarvis")
logger.setLevel(logging.DEBUG)


# This does not work because of different encoding when using accent
from core import OrderAnalyser
order = "jarvis régle le réveil pour sept heures et vingt minutes"


oa = OrderAnalyser(order)

oa.start()


# user_said = "jarvis régle le réveil pour sept heures et pour vingts minutes"
#
# order = "régle le réveil pour {{ hour }} heures et pour {{ minute }} minutes"
#
#
# def counterSubset(list1, list2):
#     """
#     check if the number of occurrences matches
#     :param list1:
#     :param list2:
#     :return:
#     """
#     c1, c2 = Counter(list1), Counter(list2)
#     for k, n in c1.items():
#         if n > c2[k]:
#             return False
#     return True
#
#
# def _spelt_order_match_brain_order_via_table(order_to_analyse, user_said):
#     list_word_user_said = user_said.split()
#     split_order_without_bracket = _get_list_word_without_bracket(order_to_analyse)
#
#     number_of_word_in_order = len(split_order_without_bracket)
#     # if all words in the list of what the user said in in the list of word in the order
#     # return len(set(split_order_without_bracket).intersection(list_word_user_said)) == number_of_word_in_order
#     return counterSubset(split_order_without_bracket, list_word_user_said)
#
#
# def _get_list_word_without_bracket(order):
#     """
#     Get an order with bracket inside like: "hello my name is {{ name }}.
#     return a list of string without bracket like ["hello", "my", "name", "is"]
#     :param order: sentence to split
#     :return: list of string without bracket
#     """
#     pattern = r"((?:{{\s*)[\w\.]+(?:\s*}}))"
#     # find everything like {{ word }}
#     matches = re.findall(pattern, order)
#     for match in matches:
#         order = order.replace(match, "")
#     # then split
#     split_order = order.split()
#     return split_order
#
# # main test
# if _spelt_order_match_brain_order_via_table(order, user_said):
#     print "order matched"
# else:
#     print "order does not match"
