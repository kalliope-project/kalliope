# coding: utf8
import logging

from flask import Flask

from core import OrderAnalyser
from core import Utils
from core.ConfigurationManager import SettingLoader
from core.ConfigurationManager.BrainLoader import BrainLoader
from core.Players import Mplayer
from core.RestAPI.FlaskAPI import FlaskAPI

logging.basicConfig()
logger = logging.getLogger("kalliope")
logger.setLevel(logging.DEBUG)


brain = BrainLoader.get_brain()
#
# order = "bonjour"
# oa = OrderAnalyser(order=order, brain=brain)
# oa.start()



app = Flask(__name__)
flask_api = FlaskAPI(app, port=5000, brain=brain)
flask_api.start()




