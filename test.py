# coding: utf8
import logging
import re
from collections import Counter

from flask import Flask
from core.RestAPI.FlaskAPI import FlaskAPI
from core import OrderAnalyser
from core.ConfigurationManager import SettingLoader
from core.ConfigurationManager import YAMLLoader
from core.ConfigurationManager.BrainLoader import BrainLoader

from neurons import Systemdate
from neurons.tasker_autoremote.tasker_autoremote import Tasker_autoremote

logging.basicConfig()
logger = logging.getLogger("kalliope")
logger.setLevel(logging.DEBUG)

# order = "quelle heure est-il"
# oa = OrderAnalyser(order=order)
# oa.start()

# SettingLoader.get_settings()
#
brain = BrainLoader.get_brain()

order = "cherche sur Wikipédia bot"

oa = OrderAnalyser(order=order, brain=brain)

oa.start()


# import wikipedia
#
# languages = wikipedia.languages().keys()
# languages = sorted(languages)
# for el in languages:
#     print "- " + el














