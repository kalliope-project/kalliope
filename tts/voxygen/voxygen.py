import logging

from core import AudioPlayer
from tts import TTS

logging.basicConfig()
logger = logging.getLogger("kalliope")


class Voxygen(TTS):
    TTS_VOICE_DEFAULT = "Michel"
    TTS_LANGUAGES_DEFAULT = "default"
    TTS_URL = "https://www.voxygen.fr/sites/all/modules/voxygen_voices/assets/proxy/index.php"

    def __init__(self):
        TTS.__init__(self)

    def say(self, words=None, voice=TTS_VOICE_DEFAULT, language=TTS_LANGUAGES_DEFAULT, cache=True):
        self.say_generic(cache, language, words, self.get_audio_voxygen, AudioPlayer.PLAYER_MP3, AudioPlayer.AUDIO_MP3_FREQUENCY, voice)

    def get_audio_voxygen(self, **kwargs):
        words = kwargs.get('words', None)
        cache = kwargs.get('cache', None)
        file_path = kwargs.get('file_path', None)
        voice = kwargs.get('voice', None)
        payload = Voxygen.get_payload(voice, words)

        return TTS.get_audio(file_path, cache, payload, self.TTS_URL)

    @staticmethod
    def get_payload(voice, words):
        return {
            "method": "redirect",
            "text": words,
            "voice": voice
        }