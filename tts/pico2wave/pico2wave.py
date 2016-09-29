import subprocess
from tts import TTS
import logging, sys


class Pico2wave(TTS):
    PICO2WAVE_LANGUAGES = dict(fr="fr-FR", us="en-US", uk="en-GB", de="de-DE", es="es-ES", it="it-IT")
    PICO2WAVE_LANGUAGES_DEFAULT = PICO2WAVE_LANGUAGES['fr']

    def __init__(self, audio_player_type=None):
        TTS.__init__(self, audio_player_type, "wav")

    def say(self, words=None, language=PICO2WAVE_LANGUAGES_DEFAULT, cache=False):
        language = self.get_voice(language)
        file_path = self.cache.get_audio_file_cache_path(words, language=language, voice="default")

        self.get_audio(words, language, file_path)
        self.play_audio(file_path, cache=cache)

    def get_voice(self, language):
        if language in self.PICO2WAVE_LANGUAGES:
            return self.PICO2WAVE_LANGUAGES[language]

        logging.warn("Cannot find language matching language: %s voice: %s replace by default voice: %s", language, self.PICO2WAVE_LANGUAGES_DEFAULT)
        return self.PICO2WAVE_LANGUAGES_DEFAULT

    @staticmethod
    def get_audio(words, language, file_path):
        subprocess.check_output(["/usr/bin/pico2wave", "-l=%s" % language, "-w=%s" % file_path, words], stderr=sys.stderr)


