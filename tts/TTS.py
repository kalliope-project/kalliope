from core import AudioPlayer
from core import Cache

import logging
import os
import requests
import sys
from core import FileManager

logging.basicConfig()
logger = logging.getLogger("jarvis")


class TTS:
    def __init__(self, cache_extension=None, volume=0.8):
        self.cache = Cache(module_name=self.__class__.__name__, cache_extension=cache_extension)
        self.audio_player = AudioPlayer(volume=volume)

    def play_audio(self, music_file, music_type, audio_frequency, cache=False):
        self.audio_player.init_play(music_type, audio_frequency)
        self.audio_player.play_audio(music_file)
        self.cache.remove_audio_file(music_file, cache)

    def say_generic(self, cache, language, words, get_audio_specific, audio_type, audio_frequency, voice=None):
        file_path = self.cache.get_audio_file_cache_path(words, language, voice)

        if get_audio_specific(language, words, file_path, cache):
            self.play_audio(file_path, audio_type, audio_frequency, cache)

    @staticmethod
    def unify_key(key):
        return key.lower()

    @staticmethod
    def get_audio(file_path, cache, payload, url, content_type_expected, timeout_expected=30):
        if not cache or not os.path.exists(file_path) or FileManager.file_is_empty(file_path):

            r = requests.get(url, params=payload, stream=True, timeout=timeout_expected)

            content_type = r.headers['Content-Type']
            logger.debug("Trying to get url: %s response code: %s and content-type: %s", r.url, r.status_code, content_type)

            try:
                if r.status_code == requests.codes.ok and content_type == content_type_expected:
                    return FileManager.write_in_file(file_path, r.content)
                else:
                    return False
            except IOError as e:
                logger.error("I/O error(%s): %s", e.errno, e.strerror)
            except ValueError:
                logger.error("Could not convert data to an integer.")
            except:
                logger.error("Unexpected error: %s", sys.exc_info()[0])
        else:
            return True
