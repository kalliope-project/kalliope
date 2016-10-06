import logging

from core import AudioPlayer
from tts import TTS

logging.basicConfig()
logger = logging.getLogger("jarvis")


class Voicerss(TTS):
    TTS_LANGUAGES_DEFAULT = 'fr-fr'
    TTS_URL = "http://www.voicerss.org/controls/speech.ashx"
    TTS_CONTENT_TYPE = "audio/mpeg"
    TTS_TIMEOUT_SEC = 30

    def __init__(self):
        TTS.__init__(self)

    def say(self, words=None, language=TTS_LANGUAGES_DEFAULT, cache=True):
        self.say_generic(cache, language, words, self.get_audio_voicerss, AudioPlayer.PLAYER_MP3, AudioPlayer.AUDIO_MP3_44100_FREQUENCY)

    def get_audio_voicerss(self, language, words, file_path, cache):
        payload = {
            "src": words,
            "hl": language,
            "c": "mp3"
        }
        return self.get_audio(file_path, cache, payload, self.TTS_URL, self.TTS_CONTENT_TYPE, self.TTS_TIMEOUT_SEC)
