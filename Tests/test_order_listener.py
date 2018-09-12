import unittest

from mock import mock

from kalliope.core import OrderListener
from kalliope.core.Models import Resources
from kalliope.core.Models.settings.Stt import Stt


class TestOrderListener(unittest.TestCase):

    """Test case for the OrderListener Class"""

    def setUp(self):
        pass

    def test_load_stt_plugin(self):

        # Test getting default stt
        ol = OrderListener()

        stt1 = Stt(name="default-stt",
                   parameters=dict())

        stt2 = Stt(name="second-stt",
                   parameters=dict())

        stt3 = Stt(name="third-stt",
                   parameters=dict())

        resources = Resources(stt_folder="/tmp")
        ol.settings = mock.MagicMock(default_stt_name="default-stt",
                                     stts=[stt1, stt2, stt3],
                                     resources=resources)

        callback = mock.MagicMock()

        ol.callback = callback

        with mock.patch("kalliope.core.Utils.get_dynamic_class_instantiation") as mock_get_dynamic_class_instantiation:
            mock_get_dynamic_class_instantiation.return_value = 'class_instance'
            self.assertEqual(ol.load_stt_plugin(),
                             "class_instance",
                             "Fail getting the proper value")

            mock_get_dynamic_class_instantiation.assert_called_once_with(package_name="stt",
                                                                         module_name="Default-stt",
                                                                         parameters={'callback': callback,
                                                                                     'audio_file_path': None},
                                                                         resources_dir="/tmp")


if __name__ == '__main__':
    unittest.main()
