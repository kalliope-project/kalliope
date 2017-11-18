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
                 random_wake_up_answers=None,
                 random_wake_up_sounds=None,
                 play_on_ready_notification=None,
                 on_ready_answers=None,
                 on_ready_sounds=None,
                 triggers=None,
                 players=None,
                 rest_api=None,
                 cache_path=None,
                 default_synapse=None,
                 resources=None,
                 variables=None,
                 rpi_settings=None,
                 recognition_options=None,
                 start_options=None):

        self.default_tts_name = default_tts_name
        self.default_stt_name = default_stt_name
        self.default_trigger_name = default_trigger_name
        self.default_player_name = default_player_name
        self.ttss = ttss
        self.stts = stts
        self.random_wake_up_answers = random_wake_up_answers
        self.random_wake_up_sounds = random_wake_up_sounds
        self.play_on_ready_notification = play_on_ready_notification
        self.on_ready_answers = on_ready_answers
        self.on_ready_sounds = on_ready_sounds
        self.triggers = triggers
        self.players = players
        self.rest_api = rest_api
        self.cache_path = cache_path
        self.default_synapse = default_synapse
        self.resources = resources
        self.variables = variables
        self.machine = platform.machine()   # can be x86_64 or armv7l
        self.kalliope_version = current_kalliope_version
        self.rpi_settings = rpi_settings
        self.recognition_options = recognition_options
        self.start_options = start_options

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
            'random_wake_up_answers': self.random_wake_up_answers,
            'random_wake_up_sounds': self.random_wake_up_sounds,
            'play_on_ready_notification': self.play_on_ready_notification,
            'on_ready_answers': self.on_ready_answers,
            'on_ready_sounds': self.on_ready_sounds,
            'triggers': self.triggers,
            'players': self.players,
            'rest_api': self.rest_api.serialize(),
            'cache_path': self.cache_path,
            'default_synapse': self.default_synapse,
            'resources': self.resources,
            'variables': self.variables,
            'machine': self.machine,
            'kalliope_version': self.kalliope_version,
            'rpi_settings': self.rpi_settings.serialize() if self.rpi_settings is not None else None,
            'recognition_options': self.recognition_options.serialize() if self.recognition_options is not None else None,
            'start_options': self.start_options,
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
