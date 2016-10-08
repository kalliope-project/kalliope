# -*- coding: utf-8 -*-

import re, math
from collections import Counter



# user_said = "maman je voudrais ecouter ACDC"
# order = "je voudrais ecouter {{ artist_name }}"

user_said = "s'il te plait regle le reveil pour dix huit heures et dix neuf  minutes trente trois  secondes cent quatre vingt dix "

user_said_list = [" regle le reveil pour neuf  heures et quinze minutes trente trois secondes ",
                 "s'il te plait regle le reveil pour dix huit huf  minutes trente trois  secondes cent quatre vingt dix ",
                 "regle pour dix huit heures et   trente trois  secondes cent quatre vingt dix ",
                 "s'il te plait regle le reveil poutes trente trois  secondes cent quatre vingt dix ",
                 "RIEN A VOIR",
                " minutes neuf trente reveil regle secondes  quinze  le heures et    trois  pour "
                  ]

order = "{{ politesse }} regle le reveil pour {{ hour}} heures et {{minute }} minutes {{ seconde  }} secondes {{mili}}"

order_list = ["regle le reveil pour  heures et  minutes  secondes ",
              "{{ politesse }} regle le reveil pour {{ hour}} heures et {{minute }} minutes {{ seconde  }} secondes {{mili}}",
              "politesse  regle le reveil pour  hour heures et minute  minutes  seconde   secondes mili",
              " reveil pour {{ hour}}  et {{minute }} minutes  secondes {{mili}}",
              "{{ politesse }} regle le reveil pour "
              ]


# take a look to each order

WORD = re.compile(r'\w+')

def get_cosine(vec1, vec2):
     intersection = set(vec1.keys()) & set(vec2.keys())
     numerator = sum([vec1[x] * vec2[x] for x in intersection])

     sum1 = sum([vec1[x]**2 for x in vec1.keys()])
     sum2 = sum([vec2[x]**2 for x in vec2.keys()])
     denominator = math.sqrt(sum1) * math.sqrt(sum2)

     if not denominator:
        return 0.0
     else:
        return float(numerator) / denominator

def text_to_vector(text):
     words = WORD.findall(text)
     return Counter(words)


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



for us in user_said_list:
    for od in order_list:
        vector1 = text_to_vector(us)
        vector2 = text_to_vector(od)

        cosine = get_cosine(vector1, vector2)

        print "Cosine -> ", cosine, " for usersaid: ",us, " ,order:", od






