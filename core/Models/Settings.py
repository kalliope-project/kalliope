

class Settings(object):
    def __init__(self, default_tts_name=None, default_stt_name=None,
                 default_trigger_name=None, ttss=None, stts=None,
                 random_wake_up_answers=None, random_wake_up_sounds=None, triggers=None, rest_api=None, cache_path=None):
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
