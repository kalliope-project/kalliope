# coding: utf8
import logging

import re

from kalliope.core.ConfigurationManager.BrainLoader import BrainLoader
from kalliope.core.ConfigurationManager.SettingLoader import SettingLoader

logging.basicConfig()
logger = logging.getLogger("kalliope")
logger.setLevel(logging.DEBUG)

# file_path = "core/Tests/brains/brain_test.yml"
#
# brainloader1 = BrainLoader.Instance(file_path=file_path)
#
# brainloader2 = BrainLoader.Instance(file_path=file_path)

# sl = SettingLoader.Instance(file_path="core/Tests/settings/settings_test.yml")
# print(sl.yaml_config)



# locate our version number
def read_version_py(file_name):
    try:
        version_string_line = open(file_name, "rt").read()
    except EnvironmentError:
        return None
    else:
        version_regex = r"^version_str = ['\"]([^'\"]*)['\"]"
        mo = re.search(version_regex, version_string_line, re.M)
        if mo:
            return mo.group(1)

VERSION_PY_FILENAME = 'kalliope/_version.py'
version = read_version_py(VERSION_PY_FILENAME)

print(version)
