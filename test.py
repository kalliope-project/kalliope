# coding=utf-8
import os

from core.ConfigurationManager import SettingLoader
from core.CrontabManager import CrontabManager
from core.OrderAnalyser import OrderAnalyser

import logging

from core.TriggerLauncher import TriggerLauncher

logging.basicConfig()
logger = logging.getLogger("jarvis")

order = "est-ce que j'ai des emails"

oa = OrderAnalyser(order=order)

oa.start()





