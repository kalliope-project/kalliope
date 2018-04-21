import unittest
import mock

from kalliope.core.Models.settings.Settings import Settings
from kalliope.core.TriggerLauncher import TriggerLauncher

from kalliope.core.Models.settings.Trigger import Trigger


class TestTriggerLauncher(unittest.TestCase):
    """
    Class to test Launchers Classes (TriggerLauncher) and methods
    """

    def setUp(self):
        pass

    ####
    # Trigger Launcher
    def test_get_trigger(self):
        """
        Test the Trigger Launcher trying to run the trigger
        """
        trigger1 = Trigger("Trigger", {})
        trigger2 = Trigger("Trigger2", {'pmdl_file': "trigger/snowboy/resources/kalliope-FR-6samples.pmdl"})
        settings = Settings()
        settings.triggers = [trigger1, trigger2]
        with mock.patch("kalliope.core.Utils.get_dynamic_class_instantiation") as mock_get_class_instantiation:
            # Get the trigger 1
            settings.default_trigger_name = "Trigger"
            TriggerLauncher.get_trigger(settings=settings,
                                        callback=None)

            mock_get_class_instantiation.assert_called_once_with(package_name="trigger",
                                                                 module_name=trigger1.name,
                                                                 parameters=trigger1.parameters)
            mock_get_class_instantiation.reset_mock()

            # Get the trigger 2
            settings.default_trigger_name = "Trigger2"
            TriggerLauncher.get_trigger(settings=settings,
                                        callback=None)

            mock_get_class_instantiation.assert_called_once_with(package_name="trigger",
                                                                 module_name=trigger2.name,
                                                                 parameters=trigger2.parameters)
            mock_get_class_instantiation.reset_mock()