import logging

from core import AudioPlayer
from tts import TTS

logging.basicConfig()
logger = logging.getLogger("jarvis")


class Voxygen(TTS):
    TTS_VOICE_DEFAULT = "Michel"
    TTS_LANGUAGES_DEFAULT = "default"
    TTS_URL = "https://www.voxygen.fr/sites/all/modules/voxygen_voices/assets/proxy/index.php"
    TTS_CONTENT_TYPE = "audio/mpeg"
    TTS_TIMEOUT_SEC = 30

    def __init__(self):
        TTS.__init__(self)

    def say(self, words=None, voice=TTS_VOICE_DEFAULT, language=TTS_LANGUAGES_DEFAULT, cache=True):
        self.say_generic(cache, language, words, self.get_audio_voxygen, AudioPlayer.PLAYER_MP3, AudioPlayer.AUDIO_MP3_FREQUENCY, voice)

    def get_audio_voxygen(self, language, words, file_path, cache, voice):
        payload = {
            "method": "redirect",
            "text": words,
            "voice": voice
        }
        return self.get_audio(file_path, cache, payload, self.TTS_URL, self.TTS_CONTENT_TYPE, self.TTS_TIMEOUT_SEC)