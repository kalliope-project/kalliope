import unittest

from core.TTS.TTSModule import TTSModule


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
