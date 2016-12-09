import unittest
import mock

from kalliope.core.NeuronModule import NeuronModule


class TestNeuronModule(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_audio_from_stt(self):
        """
        Test the OrderListener thread is started
        """

        with mock.patch("kalliope.core.OrderListener.start") as mock_orderListerner_start:
            def callback():
                pass
            NeuronModule.get_audio_from_stt(callback=callback())
            mock_orderListerner_start.assert_called_once_with()
            mock_orderListerner_start.reset_mock()

    def test_update_cache_var(self):
        """
        Test Update the value of the cache in the provided arg list
        """

        # True -> False
        args_dict = {
            "cache": True
        }
        expected_dict = {
            "cache": False
        }
        self.assertEquals(NeuronModule._update_cache_var(False, args_dict=args_dict),
                          expected_dict,
                          "Fail to update the cache value from True to False")
        self.assertFalse(args_dict["cache"])

        # False -> True
        args_dict = {
            "cache": False
        }
        expected_dict = {
            "cache": True
        }
        self.assertEquals(NeuronModule._update_cache_var(True, args_dict=args_dict),
                          expected_dict,
                          "Fail to update the cache value from False to True")

        self.assertTrue(args_dict["cache"])




