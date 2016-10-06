import logging

import re

import requests

from core import AudioPlayer
from tts import TTS

logging.basicConfig()
logger = logging.getLogger("jarvis")


class Acapela(TTS):
    TTS_LANGUAGES_DEFAULT = 'sonid15'
    TTS_VOICE_DEFAULT = 'Manon'
    TTS_URL = "http://www.acapela-group.com/demo-tts/DemoHTML5Form_V2_fr.php"
    TTS_CONTENT_TYPE = "audio/mpeg"
    TTS_TIMEOUT_SEC = 30

    def __init__(self):
        TTS.__init__(self)

    def say(self, words=None, language=TTS_LANGUAGES_DEFAULT, voice=TTS_VOICE_DEFAULT, cache=True):
        self.say_generic(cache, language, words, self.get_audio_acapela, AudioPlayer.PLAYER_MP3, AudioPlayer.AUDIO_MP3_22050_FREQUENCY, voice)

    def get_audio_acapela(self, language, words, file_path, cache, voice):
        payload = {
            "MyLanguages": language,
            "MySelectedVoice": voice,
            "MyTextForTTS": words,
            "t": "1",
            "SendToVaaS": ""
        }
        url = Acapela.get_audio_link(self.TTS_URL, payload)
        return self.get_audio(file_path, cache, payload, url, self.TTS_CONTENT_TYPE, self.TTS_TIMEOUT_SEC)

    @staticmethod
    def get_audio_link(url, payload, timeout_expected=30):
        r = requests.post(url, payload, timeout=timeout_expected)
        data = r.content
        return re.search("(?P<url>https?://[^\s]+).mp3", data).group(0)
