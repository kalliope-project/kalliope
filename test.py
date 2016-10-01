# coding=utf-8
import os

from core.CrontabManager import CrontabManager
from core.OrderAnalyser import OrderAnalyser

import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


# oa = OrderAnalyser("wake up", brain_file="/home/nico/Documents/jarvis/test.yml")
#
# oa = OrderAnalyser("test", brain_file="brain_examples/fr/fr_systemdate.yml")
#
# oa.start()

# cmd = "python jarvis.py start --run-synapse \"say hello\" --brain-file /home/nico/Documents/jarvis/test.yml"
#
# os.system(cmd)

crontab_manager = CrontabManager(brain_file="/home/nico/Documents/jarvis/test.yml")
crontab_manager.load_events_in_crontab()