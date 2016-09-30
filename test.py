# coding=utf-8
import os

from core.CrontabManager import CrontabManager
from core.OrderAnalyser import OrderAnalyser

import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


# # oa = OrderAnalyser("test", brain_file="brain_examples/fr/say_examples.yml")
#
# oa = OrderAnalyser("test", brain_file="brain_examples/fr/fr_systemdate.yml")
#
# oa.start()

# cmd = "python jarvis.py start --synapse \"this is my synapse\""
#
# os.system(cmd)

crontab_manager = CrontabManager(brain_file="test.yml")
crontab_manager.load_events_in_crontab()