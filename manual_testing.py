# coding: utf8
import logging

from core.ConfigurationManager.BrainLoader import BrainLoader
from core.ConfigurationManager.SettingLoader import SettingLoader

logging.basicConfig()
logger = logging.getLogger("kalliope")
logger.setLevel(logging.DEBUG)

file_path = "core/Tests/brains/brain_test.yml"

brainloader1 = BrainLoader.Instance(file_path=file_path)

brainloader2 = BrainLoader.Instance(file_path=file_path)

if id(brainloader1) == id(brainloader2):
    print "Same"
else:
    print "Different"


print brainloader1.yaml_config


