import hashlib
import os
import logging

from core.FileManager import FileManager


class Cache:
    DEFAULT_MODULE_NAME = "default"
    DEFAULT_CACHE_PATH = "/tmp/jarvis/tts"
    DEFAULT_CACHE_EXTENSION = "tts"
    DEFAULT_LANGUAGE = "default"
    DEFAULT_VOICE = "default"

    def __init__(self, module_name=DEFAULT_MODULE_NAME, cache_path=DEFAULT_CACHE_PATH, cache_extension=DEFAULT_CACHE_EXTENSION):
        self._module_name = module_name
        self._cache_path = cache_path
        self._cache_extension = cache_extension

    def get_audio_file_cache_path(self, words, voice, language):
        # fix UnicodeEncodeError: 'ascii' codec can't encode character X in position Y
        words = words.encode('utf-8')
        md5 = hashlib.md5(words).hexdigest()
        filename = voice + "." + md5 + self._cache_extension
        cache_directory = os.path.join(self._cache_path, self._module_name, language)
        file_path = os.path.join(cache_directory, filename)
        FileManager.create_directory(cache_directory)
        logging.debug("Cache directory %s exists and File path for audio is: %s", cache_directory, file_path)
        return file_path

    @staticmethod
    def remove_audio_file(file_path, cache):
        if not cache:
            FileManager.remove_file(file_path)

