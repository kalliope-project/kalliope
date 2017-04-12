import unittest
import mock

from kalliope.core.TriggerLauncher import TriggerLauncher

from kalliope.core.Models.Trigger import Trigger


class TestTriggerLauncher(unittest.TestCase):
    """
    Class to test Launchers Classes (TriggerLauncher, SynapseLauncher, NeuronLauncher) and methods
    """

    def setUp(self):
        pass

    ####
    # Trigger Launcher
    def test_get_trigger(self):
        """
        Test the Trigger Launcher trying to run the trigger
        """
        trigger = Trigger("Trigger", {})
        with mock.patch("kalliope.core.Utils.get_dynamic_class_instantiation") as mock_get_class_instantiation:
            TriggerLauncher.get_trigger(trigger=trigger,
                                        callback=None)

            mock_get_class_instantiation.assert_called_once_with(package_name="trigger",
                                                                 module_name=trigger.name,
                                                                 parameters=trigger.parameters)
            mock_get_class_instantiation.reset_mock()