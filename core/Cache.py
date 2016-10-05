import hashlib
import os
import logging

from core.FileManager import FileManager

DEFAULT_MODULE_NAME = "default"
DEFAULT_CACHE_PATH = "/tmp/jarvis/tts"
DEFAULT_CACHE_EXTENSION = "tts"
DEFAULT_LANGUAGE = "default"
DEFAULT_VOICE = "default"

logging.basicConfig()
logger = logging.getLogger("jarvis")


class Cache:
    def __init__(self, module_name=DEFAULT_MODULE_NAME, cache_path=DEFAULT_CACHE_PATH,
                 cache_extension=None):
        if cache_extension is None:
            cache_extension = DEFAULT_CACHE_EXTENSION

        self._module_name = module_name
        self._cache_path = cache_path
        self._cache_extension = cache_extension

    def get_audio_file_cache_path(self, words, language=DEFAULT_LANGUAGE, voice=DEFAULT_VOICE):
        # fix UnicodeEncodeError: 'ascii' codec can't encode character X in position Y
        md5 = self.generate_md5_from_words(words)
        filename = voice + "." + md5 + "." + self._cache_extension
        cache_directory = os.path.join(self._cache_path, self._module_name, language)
        file_path = os.path.join(cache_directory, filename)
        FileManager.create_directory(cache_directory)
        logger.debug("Cache directory %s exists and File path for audio is: %s", cache_directory, file_path)
        return file_path

    @staticmethod
    def generate_md5_from_words(words):
        if isinstance(words, unicode):
            words = words.encode('utf-8')
        return hashlib.md5(words).hexdigest()

    @staticmethod
    def remove_audio_file(file_path, cache):
        if not cache:
            FileManager.remove_file(file_path)
