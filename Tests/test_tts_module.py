import os
import unittest

import mock

from kalliope.core.Models.Settings import Settings
from kalliope.core.TTS.TTSModule import TTSModule, TtsGenerateAudioFunctionNotFound
from kalliope.core.Utils.FileManager import FileManager


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
        def new_play_audio(TTSModule):
            pass

        words = "kalliope"

        with mock.patch.object(TTSModule, 'play_audio', new=new_play_audio):
            settings = Settings(cache_path="/tmp/kalliope/tests")
            self.TTSMod.settings = settings

            # test missing callback
            with self.assertRaises(TtsGenerateAudioFunctionNotFound):
                self.TTSMod.generate_and_play(words=words)

            # Assert Callback is called
            # no Cache
            self.TTSMod.cache = False
            generate_audio_function_from_child = mock.Mock()
            self.TTSMod.generate_and_play(words=words,
                                          generate_audio_function_from_child=generate_audio_function_from_child)
            generate_audio_function_from_child.assert_called()

            # with cache True but not existing on system
            self.TTSMod.cache = True
            generate_audio_function_from_child = mock.Mock()
            self.TTSMod.generate_and_play(words=words,
                                          generate_audio_function_from_child=generate_audio_function_from_child)
            generate_audio_function_from_child.assert_called()

            # with cache True and existing on system
            # create tmp file
            tmp_base_path = "/tmp/kalliope/tests/TTSModule/tests/default/"
            file_path = os.path.join(tmp_base_path, "5c186d1e123be2667fb5fd54640e4fd0.tts")
            if os.path.isfile(file_path):
                # Remove the file
                FileManager.remove_file(file_path)
            if not os.path.exists(tmp_base_path):
                os.makedirs(tmp_base_path)
            FileManager.write_in_file(file_path, "[kalliope-test] test_generate_and_play")
            self.TTSMod.cache = True
            generate_audio_function_from_child = mock.Mock()
            self.TTSMod.generate_and_play(words=words,
                                          generate_audio_function_from_child=generate_audio_function_from_child)
            generate_audio_function_from_child.assert_not_called()
            # Remove the tmp file
            FileManager.remove_file(file_path)

    def test_is_file_already_in_cache(self):
        """
        Test if file is already stored in cache
        """

        base_cache_path = "/tmp/kalliope/tests/TTSModule/tests/default/"
        md5_word = "5c186d1e123be2667fb5fd54640e4fd0"
        file_path = os.path.join(base_cache_path, "5c186d1e123be2667fb5fd54640e4fd0.tts")

        if os.path.isfile(file_path):
            # Remove the file
            FileManager.remove_file(file_path)
        # Create a tmp file
        if not os.path.exists(base_cache_path):
            os.makedirs(base_cache_path)
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

if __name__ == '__main__':
    unittest.main()
