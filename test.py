# coding: utf8
import logging
import re
from collections import Counter

from core import OrderAnalyser
from core.ConfigurationManager import YAMLLoader
from neurons import Systemdate
from neurons.tasker_autoremote.tasker_autoremote import Tasker_autoremote

logging.basicConfig()
logger = logging.getLogger("kalliope")
logger.setLevel(logging.DEBUG)

order = "playbook"
oa = OrderAnalyser(order=order)
oa.start()








