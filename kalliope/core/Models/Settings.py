import platform
from kalliope._version import version_str as current_kalliope_version


class Settings(object):
    """
    This Class is a Singleton Representing the settings.yml file with synapse

    .. note:: the is_loaded Boolean is True when the Settings has been properly loaded.
    """
    def __init__(self,
                 default_tts_name=None,
                 default_stt_name=None,
                 default_trigger_name=None,
                 ttss=None,
                 stts=None,
                 random_wake_up_answers=None,
                 random_wake_up_sounds=None,
                 triggers=None,
                 rest_api=None,
                 cache_path=None,
                 default_synapse=None,
                 resources=None,
                 machine=None,
                 kalliope_version=None):

        self.default_tts_name = default_tts_name
        self.default_stt_name = default_stt_name
        self.default_trigger_name = default_trigger_name
        self.ttss = ttss
        self.stts = stts
        self.random_wake_up_answers = random_wake_up_answers
        self.random_wake_up_sounds = random_wake_up_sounds
        self.triggers = triggers
        self.rest_api = rest_api
        self.cache_path = cache_path
        self.default_synapse = default_synapse
        self.resources = resources
        self.machine = platform.machine()   # can be x86_64 or armv7l
        self.kalliope_version = current_kalliope_version

    def __eq__(self, other):
        """
        This is used to compare 2 objects
        :param other:
        :return:
        """
        return self.__dict__ == other.__dict__
