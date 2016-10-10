import logging

import re

import requests

from core import AudioPlayer
from tts import TTS

logging.basicConfig()
logger = logging.getLogger("kalliope")


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

    def get_audio_acapela(self, **kwargs):
        language = kwargs.get('language', None)
        words = kwargs.get('words', None)
        cache = kwargs.get('cache', None)
        file_path = kwargs.get('file_path', None)
        voice = kwargs.get('voice', None)
        payload = Acapela.get_payload(language, voice, words)
        url = Acapela.get_audio_link(self.TTS_URL, payload)

        return TTS.get_audio(file_path, cache, payload, url)

    @staticmethod
    def get_audio_link(url, payload, timeout_expected=30):
        r = requests.post(url, payload, timeout=timeout_expected)
        data = r.content
        return re.search("(?P<url>https?://[^\s]+).mp3", data).group(0)

    @staticmethod
    def get_payload(language, voice, words):
        return {
            "MyLanguages": language,
            "MySelectedVoice": voice,
            "MyTextForTTS": words,
            "t": "1",
            "SendToVaaS": ""
        }
