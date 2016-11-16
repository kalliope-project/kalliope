# coding: utf8
import logging

from core.ConfigurationManager.BrainLoader import BrainLoader
from core.ConfigurationManager.SettingLoader import SettingLoader

logging.basicConfig()
logger = logging.getLogger("kalliope")
logger.setLevel(logging.DEBUG)

# file_path = "core/Tests/brains/brain_test.yml"
#
# brainloader1 = BrainLoader.Instance(file_path=file_path)
#
# brainloader2 = BrainLoader.Instance(file_path=file_path)

sl = SettingLoader.Instance(file_path="core/Tests/settings/settings_test.yml")
print sl.yaml_config




