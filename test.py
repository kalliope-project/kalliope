# coding=utf-8
import os

from core.ConfigurationManager import SettingLoader
from core.CrontabManager import CrontabManager
from core.OrderAnalyser import OrderAnalyser

import logging

from core.TriggerLauncher import TriggerLauncher

logging.basicConfig()
logger = logging.getLogger("jarvis")


# oa = OrderAnalyser("wake up", brain_file="/home/nico/Documents/jarvis/test.yml")
#
# oa = OrderAnalyser("test", brain_file="brain_examples/fr/fr_systemdate.yml")
#
# oa.start()




