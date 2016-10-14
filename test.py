# coding: utf8
import logging
import re
from collections import Counter

from core import OrderAnalyser
from neurons.tasker_autoremote.tasker_autoremote import Tasker_autoremote

logging.basicConfig()
logger = logging.getLogger("kalliope")
logger.setLevel(logging.DEBUG)


# # This does not work because of different encoding when using accent
# from core import OrderAnalyser
# # order = "kalliope régle le réveil pour sept heures et vingt minutes"
# # order = "mais nous de la musique"
#
# order = "arrête la musique"
# # order = order.decode('utf-8')
# # print type(order)
# oa = OrderAnalyser(order)
#
# oa.start()
key = "mykey"
message = "lost my phone"

tk = Tasker_autoremote(key=key, message=message)





