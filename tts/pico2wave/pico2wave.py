import subprocess

from core import AudioPlayer
from tts import TTS
import logging
import sys

logging.basicConfig()
logger = logging.getLogger("kalliope")


class Pico2wave(TTS):
    TTS_LANGUAGES_DEFAULT = 'fr-FR'

    def __init__(self):
        TTS.__init__(self, AudioPlayer.PLAYER_WAV)

    def say(self, words=None, language=TTS_LANGUAGES_DEFAULT, cache=False):
        self.say_generic(cache, language, words, self.get_audio_pico2wave, AudioPlayer.PLAYER_WAV, AudioPlayer.AUDIO_MP3_FREQUENCY)

    @staticmethod
    def get_audio_pico2wave(**kwargs):
        language = kwargs.get('language', None)
        words = kwargs.get('words', None)
        file_path = kwargs.get('file_path', None)

        subprocess.check_output(["/usr/bin/pico2wave", "-l=%s" % language, "-w=%s" % file_path, words], stderr=sys.stderr)
        return True
