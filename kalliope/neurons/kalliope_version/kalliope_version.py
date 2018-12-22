import re
from packaging import version
from kalliope._version import version_str
import requests

from kalliope.core import NeuronModule

KALLIOPE_PROJECT_MASTER_VERSION_URL = "https://raw.githubusercontent.com/kalliope-project/kalliope" \
                                      "/master/kalliope/_version.py"


class Kalliope_version(NeuronModule):

    def __init__(self, **kwargs):
        super(Kalliope_version, self).__init__(**kwargs)
        new_version_available = False
        last_master_version = None
        # get the last version online
        response = requests.get(KALLIOPE_PROJECT_MASTER_VERSION_URL)

        regex_version = r"(\d\.\d(\.\d)?(\.\d)?)"

        version_search = re.search(regex_version, response.text)
        if version_search:
            last_master_version = version_search.group(1)

        current_version = version_str

        if last_master_version:
            if version.parse(current_version) < version.parse(last_master_version):
                new_version_available = True

        message = {
            "current_version": current_version,
            "new_version_available": new_version_available,
            "last_master_version": last_master_version
        }

        self.say(message)
