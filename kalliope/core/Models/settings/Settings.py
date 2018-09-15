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
                 default_player_name=None,
                 ttss=None,
                 stts=None,
                 triggers=None,
                 players=None,
                 rest_api=None,
                 cache_path=None,
                 resources=None,
                 variables=None,
                 options=None,
                 hooks=None,
                 send_anonymous_usage_stats=None):

        self.default_tts_name = default_tts_name
        self.default_stt_name = default_stt_name
        self.default_trigger_name = default_trigger_name
        self.default_player_name = default_player_name
        self.ttss = ttss
        self.stts = stts
        self.triggers = triggers
        self.players = players
        self.rest_api = rest_api
        self.cache_path = cache_path
        self.resources = resources
        self.variables = variables
        self.machine = platform.machine()   # can be x86_64 or armv7l
        self.kalliope_version = current_kalliope_version
        self.options = options
        self.hooks = hooks
        self.send_anonymous_usage_stats = send_anonymous_usage_stats

    def serialize(self):
        """
        This method allows to serialize in a proper way this object

        :return: A dict of order
        :rtype: Dict
        """
        return {
            'default_tts_name': self.default_tts_name,
            'default_stt_name': self.default_stt_name,
            'default_trigger_name': self.default_trigger_name,
            'default_player_name': self.default_player_name,
            'ttss': [e.serialize() for e in self.ttss],
            'stts': [e.serialize() for e in self.stts],
            'triggers': [e.serialize() for e in self.triggers],
            'players': [e.serialize() for e in self.players],
            'rest_api': self.rest_api.serialize(),
            'cache_path': self.cache_path,
            'resources': self.resources.serialize(),
            'variables': self.variables,
            'machine': self.machine,
            'kalliope_version': self.kalliope_version,
            'options': self.options.serialize(),
            'hooks': self.hooks,
            'send_anonymous_usage_stats': self.send_anonymous_usage_stats
        }

    def __str__(self):
        return str(self.serialize())

    def __eq__(self, other):
        """
        This is used to compare 2 objects
        :param other:
        :return:
        """
        return self.__dict__ == other.__dict__
