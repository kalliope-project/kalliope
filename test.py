# coding: utf8
import logging

from core.ConfigurationManager.BrainLoader import BrainLoader
from core.ConfigurationManager.SettingLoader import SettingLoader

logging.basicConfig()
logger = logging.getLogger("kalliope")
logger.setLevel(logging.DEBUG)


brain = BrainLoader.get_brain()

brain2 = BrainLoader.get_brain()
brain3 = BrainLoader.get_brain()
brain4 = BrainLoader.get_brain()


print brain is brain2
print brain is brain3
print brain is brain4
print brain4 is brain2

set = SettingLoader.get_settings()
set2 = SettingLoader.get_settings()
set3 = SettingLoader.get_settings()
set4 = SettingLoader.get_settings()

print set is set2
print set is set3
print set is set4
print set3 is set2

