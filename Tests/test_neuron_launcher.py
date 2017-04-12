import unittest
import mock

from kalliope.core.Models.Resources import Resources
from kalliope.core.NeuronLauncher import NeuronLauncher
from kalliope.core.ConfigurationManager import SettingLoader

from kalliope.core.Models.Neuron import Neuron


class TestNeuronLauncher(unittest.TestCase):
    """
    Class to test Launchers Classes (TriggerLauncher, SynapseLauncher, NeuronLauncher) and methods
    """

    def setUp(self):
        pass

    ####
    # Neurons Launcher
    def test_start_neuron(self):
        """
        Test the Neuron Launcher trying to start a Neuron
        """
        neuron = Neuron(name='neurone1', parameters={'var1': 'val1'})
        sl = SettingLoader()
        resources = Resources(neuron_folder='/var/tmp/test/resources')
        sl.settings.resources = resources
        with mock.patch("kalliope.core.Utils.get_dynamic_class_instantiation") as mock_get_class_instantiation:
            NeuronLauncher.start_neuron(neuron=neuron)

            mock_get_class_instantiation.assert_called_once_with(package_name="neurons",
                                                                 module_name=neuron.name,
                                                                 parameters=neuron.parameters,
                                                                 resources_dir=sl.settings.resources.neuron_folder)
            mock_get_class_instantiation.reset_mock()


