# coding: utf8
import logging

from core import OrderAnalyser
from core.ConfigurationManager import BrainLoader
from core.ConfigurationManager.SettingLoader import SettingLoader

logging.basicConfig()
logger = logging.getLogger("kalliope")
logger.setLevel(logging.DEBUG)

brain_to_test = "neurons/uri/tests/uri_test_brain.yml"
bl = BrainLoader.Instance(file_path=brain_to_test)

order = "test-post-url"

oa = OrderAnalyser(order, brain=bl.brain)

oa.start()



