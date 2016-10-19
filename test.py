# coding: utf8
import logging
import re
from collections import Counter

from flask import Flask

from core import OrderAnalyser
from core.ConfigurationManager import SettingLoader
from core.ConfigurationManager import YAMLLoader
from core.ConfigurationManager.BrainLoader import BrainLoader
from core.RestAPI.FlaskAPI import FlaskAPI
from neurons import Systemdate
from neurons.tasker_autoremote.tasker_autoremote import Tasker_autoremote

logging.basicConfig()
logger = logging.getLogger("kalliope")
logger.setLevel(logging.DEBUG)

# order = "quelle heure est-il"
# oa = OrderAnalyser(order=order)
# oa.start()




app = Flask(__name__)
flask_api = FlaskAPI(app)
flask_api.start()










