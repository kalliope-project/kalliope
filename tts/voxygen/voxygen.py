import os

import requests
import logging
import sys

from core import AudioPlayer
from core import FileManager
from tts import TTS


class Voxygen(TTS):
    VOXYGEN_LANGUAGES = dict(
        fr=dict(electra="Electra", emma="Emma", becool="Becool", agnes="Agnes", loic="Loic", fabienne="Fabienne", helene="Helene", marion="Marion",
                matteo="Matteo",
                melodine="Melodine", mendoo="Mendoo", michel="Michel", moussa="Moussa", philippe="Philippe", sorciere="Sorciere"),
        ar=dict(adel="Adel"),
        de=dict(matthias="Matthias", jylvia="Sylvia"),
        uk=dict(bronwen="Bronwen", elizabeth="elizabeth", judith="Judith", paul="Paul", witch="Witch"),
        us=dict(bruce="Bruce", jenny="Jenny"),
        es=dict(martha="Martha"),
        it=dict(sonia="Sonia"))

    VOXYGEN_VOICE_DEFAULT = "Michel"
    VOXYGEN_LANGUAGES_DEFAULT = "default"
    VOXYGEN_URL = "https://www.voxygen.fr/sites/all/modules/voxygen_voices/assets/proxy/index.php"
    VOXYGEN_CONTENT_TYPE = "audio/mpeg"
    VOXYGEN_TIMEOUT_SEC = 30

    def __init__(self):
        TTS.__init__(self, AudioPlayer.PLAYER_MP3)

    def say(self, words=None, voice=None, language=VOXYGEN_LANGUAGES_DEFAULT, cache=True):
        voice = self.get_voice(voice, language)

        file_path = self.cache.get_audio_file_cache_path(words, voice, language)

        if self.get_audio(voice, words, file_path, cache):
            self.play_audio(file_path)
            self.cache.remove_audio_file(file_path, cache)

    def get_voice(self, voice, language):
        if language in self.VOXYGEN_LANGUAGES and voice in self.VOXYGEN_LANGUAGES[language]:
            return self.VOXYGEN_LANGUAGES[language][voice]

        logging.warn("Cannot find language matching language: %s voice: %s replace by default voice: %s", language, voice, self.VOXYGEN_VOICE_DEFAULT)
        return self.VOXYGEN_VOICE_DEFAULT

    def get_audio(self, voice, words, file_path, cache):
        if not cache or not os.path.exists(file_path) or FileManager.file_is_empty(file_path):
            payload = {
                "method": "redirect",
                "text": words.encode('utf8'),
                "voice": voice
            }

            r = requests.get(self.VOXYGEN_URL, params=payload, stream=True, timeout=self.VOXYGEN_TIMEOUT_SEC)

            content_type = r.headers['Content-Type']
            logging.debug("Trying to get url: %s response code: %s and content-type: %s", r.url, r.status_code, content_type)

            try:
                if r.status_code == requests.codes.ok and content_type == self.VOXYGEN_CONTENT_TYPE:
                    return FileManager.write_in_file(file_path, r.content)
                else:
                    return False
            except IOError as e:
                logging.error("I/O error(%s): %s", e.errno, e.strerror)
            except ValueError:
                logging.error("Could not convert data to an integer.")
            except:
                logging.error("Unexpected error: %s", sys.exc_info()[0])
        else:
            return True
