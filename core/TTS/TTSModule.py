# coding: utf8
import logging

logging.basicConfig()
logger = logging.getLogger("kalliope")


class TTSModule(object):

    def __init__(self):
        """
        Mother class of TTS module. Hnadle:
        - Cache: call cache object to create file, delete file, check if file exist

        - Player: call the default player to play the generated file
        """

    def play_audio(self, audio_file_path):
        """

        :param audio_file_path:
        :return:
        """

    def get_path_to_store_audio(self, text):
        """
        Call the cache to get the valid path where the TTS module will store the downloaded or generated file
        :param text: String text audio we want to save on the local disk
        :return:
        """
        # TODO: question: maybe we can implement function in cache directly in TTSModule as it is its job anyway to do all that stuff?
        pass