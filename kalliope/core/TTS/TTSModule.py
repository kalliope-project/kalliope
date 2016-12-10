# coding: utf8
import hashlib
import logging
import os

from kalliope.core.ConfigurationManager import SettingLoader
from kalliope.core.Players import Mplayer
from kalliope.core.Utils.FileManager import FileManager

logging.basicConfig()
logger = logging.getLogger("kalliope")


class MissingTTSParameter(Exception):
    """
    Some TTS Parameters are missing in the settings.yml file.

    .. seealose:: Settings
    """
    pass


class TtsGenerateAudioFunctionNotFound(Exception):
    """
    You must provide a callBack to the TTS
    """
    pass


class FailToLoadSoundFile(Exception):
    """
    Fail while truing to load the sound file.
    """
    pass


class TTSModule(object):
    """
    Mother class of TTS module. Handle:
    - Cache: call cache object to create file, delete file, check if file exist
    - Player: call the default player to play the generated file
    """

    def __init__(self, **kwargs):

        # set parameter from what we receive from the settings
        self.cache = kwargs.get('cache', False)
        self.language = kwargs.get('language', None)
        self.voice = kwargs.get('voice', "default")
        # the name of the TSS is the name of the Tss module that have instantiated TTSModule
        self.tts_caller_name = self.__class__.__name__

        # we don't know yet the words that will be converted to an audio and so we don't have the audio path yet too
        self.words = None
        self.file_path = None
        self.base_cache_path = None

        # load settings
        sl = SettingLoader()
        self.settings = sl.settings

        # create the path in the tmp folder
        base_path = os.path.join(self.settings.cache_path, self.tts_caller_name, self.language, self.voice)
        FileManager.create_directory(base_path)

        logger.debug("Class TTSModule called from module %s, cache: %s, language: %s, voice: %s" % (self.tts_caller_name,
                                                                                                     self.cache,
                                                                                                     self.language,
                                                                                                     self.voice))

    def play_audio(self):
        """
        Play the audio file
        """
        Mplayer.play(self.file_path)

    def generate_and_play(self, words, generate_audio_function_from_child=None):
        """
        Generate an audio file from <words> if not already in cache and call the Player to play it
        :param words: Sentence text from which we want to generate an audio file
        :type words: String
        :param generate_audio_function_from_child: The child function to generate a file if necessary
        :type generate_audio_function_from_child; Callback function

        .. raises:: TtsGenerateAudioFunctionNotFound
        """
        if generate_audio_function_from_child is None:
            raise TtsGenerateAudioFunctionNotFound

        self.words = words
        # we can generate the file path from info we have
        self.file_path = self._get_path_to_store_audio()

        if not self.cache:
            # no cache, we need to generate the file
            generate_audio_function_from_child()
        else:
            # we check if the file already exist. If not we generate it with the TTS engine
            if not self._is_file_already_in_cache(self.base_cache_path, self.file_path):
                generate_audio_function_from_child()

        # then play the generated audio file
        self.play_audio()

        # if the user don't want to keep the cache we remove the file
        if not self.cache:
            FileManager.remove_file(self.file_path)

    def _get_path_to_store_audio(self):
        """
        Get a sentence (a text) an return the full path of the file

        Path syntax:
        </path/in/settings>/<tts.name>/tts.parameter["language"]/tts.parameter["voice"]/<md5_of_sentence.tts

        E.g:
        /tmp/kalliope/voxygene/fr/abcd12345.tts

        :return: path String
        """
        md5 = self.generate_md5_from_words(self.words)+".tts"
        self.base_cache_path = os.path.join(self.settings.cache_path, self.tts_caller_name, self.language, self.voice)

        returned_path = os.path.join(self.base_cache_path, md5)
        logger.debug("get_path_to_store_audio return: %s" % returned_path)
        return returned_path

    @staticmethod
    def generate_md5_from_words(words):
        """
        Generate a md5 hash from received text
        :param words: Text to convert into md5 hash
        :return: String md5 hash from the received words
        """
        if isinstance(words, unicode):
            words = words.encode('utf-8')
        return hashlib.md5(words).hexdigest()

    @staticmethod
    def _is_file_already_in_cache(base_cache_path, file_path):
        """
        Return true if the file to generate has already been generated before
        """
        # generate sub folder
        FileManager.create_directory(base_cache_path)

        # check if the audio file exist
        exist_in_cache = os.path.exists(file_path)

        if exist_in_cache:
            logger.debug("TTSModule, File already in cache: %s" % file_path)
        else:
            logger.debug("TTSModule, File not yet in cache: %s" % file_path)
        return exist_in_cache
