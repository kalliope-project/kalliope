import shutil
import hashlib
import os
import logging


class Cache:
    DEFAULT_MODULE_NAME = "default"
    DEFAULT_CACHE_PATH = "/tmp/jarvis/tts"
    DEFAULT_CACHE_EXTENSION = ".tts"

    def __init__(self, module_name=DEFAULT_MODULE_NAME, cache_path=DEFAULT_CACHE_PATH, cache_extension=DEFAULT_CACHE_EXTENSION):
        self._module_name = module_name
        self._cache_path = cache_path
        self._cache_extension = cache_extension

    def get_audio_file_cache_path(self, words, voice, language):
        md5 = hashlib.md5(words).hexdigest()
        filename = voice + "." + md5 + self._cache_extension
        cache_directory = os.path.join(self._cache_path, self._module_name, language)
        file_path = os.path.join(cache_directory, filename)
        self.create_directory(cache_directory)
        logging.debug("Cache directory %s exists and File path for audio is: %s", cache_directory, file_path)
        return file_path

    @staticmethod
    def create_directory(cache_path):
        if not os.path.exists(cache_path):
            os.makedirs(cache_path)

    def write_in_file(self, file_path, content):
        with open(file_path, "wb") as file_open:
            file_open.write(content)
            file_open.close()
        return not self.file_is_empty(file_path)

    def wipe_cache(self):
        shutil.rmtree(self._cache_path)

    @staticmethod
    def file_is_empty(file_path):
        return os.path.getsize(file_path) == 0
