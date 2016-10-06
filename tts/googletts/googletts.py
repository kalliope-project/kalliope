import logging

from core import AudioPlayer
from tts import TTS

logging.basicConfig()
logger = logging.getLogger("jarvis")


class Googletts(TTS):
    TTS_LANGUAGES_DEFAULT = 'fr'
    TTS_URL = "http://translate.google.com/translate_tts"
    TTS_CONTENT_TYPE = "audio/mpeg"
    TTS_TIMEOUT_SEC = 30

    def __init__(self):
        TTS.__init__(self)

    def say(self, words=None, language=TTS_LANGUAGES_DEFAULT, cache=True):
        self.say_generic(cache, language, words, self.get_audio_googletts, AudioPlayer.PLAYER_MP3, 25000)

    def get_audio_googletts(self, language, words, file_path, cache):
        payload = {
            "q": words,
            "tl": language,
            "ie": "UTF-8",
            "total": "1",
            "client": "tw-ob"
        }
        return self.get_audio(file_path, cache, payload, self.TTS_URL, self.TTS_CONTENT_TYPE, self.TTS_TIMEOUT_SEC)
