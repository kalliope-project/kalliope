# coding: utf8
import logging

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





