# coding: utf8
import logging

from core.ConfigurationManager.BrainLoader import BrainLoader
from core.ConfigurationManager.SettingLoader import SettingLoader

logging.basicConfig()
logger = logging.getLogger("kalliope")
logger.setLevel(logging.DEBUG)


brain = BrainLoader.get_brain()
print brain.brain_yaml
for synapse in brain.synapses:
    print "test"
    print synapse.name

