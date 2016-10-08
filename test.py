# -*- coding: utf-8 -*-
import os

import re


import logging



# user_said = "maman je voudrais ecouter ACDC"
# order = "je voudrais ecouter {{ artist_name }}"

user_said = "s'il te plait regle le reveil pour dix huit heures et dix neuf  minutes trente trois  secondes cent quatre vingt dix "
order = "regle le reveil pour {{ hour}} heures et {{minute }} minutes {{ seconde  }} secondes {{mili}}"


# take a look to each order


def _is_containing_bracket(sentence):
    # print "sentence to test %s" % sentence
    pattern = r"{{|}}"
    # prog = re.compile(pattern)
    bool = re.search(pattern, sentence)
    if bool is not None:
        return True
    return False


def _get_next_value_list(list):
    ite = list.__iter__()
    next(ite, None)
    return next(ite, None)

# check if the order contain bracket
if _is_containing_bracket(order):
    # remove white space between {{ and }}
    # get a table of word said
    list_word_in_order = re.sub('\s+(?=[^\{\{\}\}]*\}\})', '',order).split()
    print "order matched: %s" % list_word_in_order

    # get the order, defined by the first words before {{
    the_order = order[:order.find('{{')]
    print "the order catched %s" % the_order


    # remove sentence before order
    nb = user_said[user_said.find(the_order):]
    truncate_list_word_said = nb.split()
    print "truncate_list_word_said : %s" % truncate_list_word_said


    # make dict var:value
    dictVar = {}
    for idx, ow in enumerate(list_word_in_order):
        if _is_containing_bracket(ow):
            # remove bracket et key dict
            varname = ow.replace("{{","").replace("}}", "")
            stopValue = _get_next_value_list(list_word_in_order[idx:])
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
    print "The dict Var : %s" % dictVar










