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
                 recognition_options=None,
                 options=None,
                 hooks=None):

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
        self.recognition_options = recognition_options
        self.options = options
        self.hooks = hooks

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
            'ttss': self.ttss,
            'stts': self.stts,
            'triggers': self.triggers,
            'players': self.players,
            'rest_api': self.rest_api.serialize(),
            'cache_path': self.cache_path,
            'resources': self.resources,
            'variables': self.variables,
            'machine': self.machine,
            'kalliope_version': self.kalliope_version,
            'recognition_options': self.recognition_options.serialize() if self.recognition_options is not None else None,
            'options': self.options,
            'hooks': self.hooks
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
