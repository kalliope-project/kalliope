import logging

from core import AudioPlayer
from tts import TTS

logging.basicConfig()
logger = logging.getLogger("kalliope")


class Googletts(TTS):
    TTS_LANGUAGES_DEFAULT = 'fr'
    TTS_URL = "http://translate.google.com/translate_tts"
    TTS_CONTENT_TYPE = "audio/mpeg"
    TTS_TIMEOUT_SEC = 30

    def __init__(self):
        TTS.__init__(self)

    def say(self, words=None, language=TTS_LANGUAGES_DEFAULT, cache=True):
        self.say_generic(cache, language, words, self.get_audio_googletts, AudioPlayer.PLAYER_MP3, 25000)

    def get_audio_googletts(self, **kwargs):
        words = kwargs.get('words', None)
        cache = kwargs.get('cache', None)
        file_path = kwargs.get('file_path', None)
        language = kwargs.get('language', None)
        payload = Googletts.get_payload(language,words)

        return TTS.get_audio(file_path, cache, payload, self.TTS_URL)

    @staticmethod
    def get_payload(language, words):
        return {
            "q": words,
            "tl": language,
            "ie": "UTF-8",
            "total": "1",
            "client": "tw-ob"
        }