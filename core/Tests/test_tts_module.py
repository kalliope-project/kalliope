import unittest
import os

from core.TTS.TTSModule import TTSModule
from core.Models.Settings import Settings
from core.FileManager import FileManager


class TestTTSModule(unittest.TestCase):
    """
    Class to test TTSModule
    """

    def setUp(self):
        self.TTSMod = TTSModule(language='tests')
        pass

    def test_generate_md5_from_words(self):
        """
        Test generate md5 method
        """

        word = "kalliope"
        expected_result = "5c186d1e123be2667fb5fd54640e4fd0"

        self.assertEquals(TTSModule.generate_md5_from_words(words=word),
                          expected_result,
                          "Fail md5")

    def test_get_path_to_store_audio(self):
        """
        Test the path to store audio
        """

        self.TTSMod.words = "kalliope"
        settings = Settings(cache_path="/tmp/kalliope/tests")
        self.TTSMod.settings = settings

        expected_result = "/tmp/kalliope/tests/TTSModule/tests/default/5c186d1e123be2667fb5fd54640e4fd0.tts"

        self.assertEquals(self.TTSMod._get_path_to_store_audio(),
                          expected_result,
                          "fail test_get_path_to_store_audio, expected path not corresponding to result")

    def test_generate_and_play(self):
        """
        Test to generate and play sound
        """
        def play_audio():
            pass

        # self.TTSMod.words = "kalliope"
        # settings = Settings(cache_path="/tmp/kalliope/tests")
        # self.TTSMod.settings = settings
        # self.TTSMod.play_audio


    def test_is_file_already_in_cache(self):
        """
        Test if file is already stored in cache
        """

        base_cache_path = "/tmp/kalliope/tests/TTSModule/tests/default/"
        md5_word = "5c186d1e123be2667fb5fd54640e4fd0"
        file_path = "/tmp/kalliope/tests/TTSModule/tests/default/5c186d1e123be2667fb5fd54640e4fd0.tts"

        # Create a tmp file
        tmp_path = os.path.join(base_cache_path, md5_word+".tts")
        FileManager.write_in_file(tmp_path, "[kalliope-test] test_is_file_already_in_cache")

        # Test true
        self.assertTrue(TTSModule._is_file_already_in_cache(base_cache_path=base_cache_path, file_path=file_path),
                        "Fail retrieving the cached file. The file does not exist but it should !")

        # Remove the tmp file
        FileManager.remove_file(tmp_path)

        # Test False
        self.assertFalse(TTSModule._is_file_already_in_cache(base_cache_path=base_cache_path, file_path=file_path),
                         "Fail asserting that the file does not exist.")
