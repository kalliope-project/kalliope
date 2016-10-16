# coding: utf8
import logging
import re
from collections import Counter

from core import OrderAnalyser
from neurons import Systemdate
from neurons.tasker_autoremote.tasker_autoremote import Tasker_autoremote

logging.basicConfig()
logger = logging.getLogger("kalliope")
logger.setLevel(logging.DEBUG)


# order = "musique rock"
# order = "stop la musique"
order = "rm file"
oa = OrderAnalyser(order)
oa.start()







