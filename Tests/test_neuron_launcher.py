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
    def test_launch_neuron(self):
        """
        Test the Neuron Launcher trying to start a Neuron
        """
        neuron = Neuron(name='neurone1', parameters={'var1': 'val1'})
        sl = SettingLoader()
        resources = Resources(neuron_folder='/var/tmp/test/resources')
        sl.settings.resources = resources
        with mock.patch("kalliope.core.Utils.get_dynamic_class_instantiation") as mock_get_class_instantiation:
            NeuronLauncher.launch_neuron(neuron=neuron)

            mock_get_class_instantiation.assert_called_once_with(package_name="neurons",
                                                                 module_name=neuron.name,
                                                                 parameters=neuron.parameters,
                                                                 resources_dir=sl.settings.resources.neuron_folder)
            mock_get_class_instantiation.reset_mock()

    def test_start_neuron(self):
        """
        Testing params association and starting a Neuron
        """

        with mock.patch("kalliope.core.NeuronLauncher.launch_neuron") as mock_launch_neuron_method:
            # Assert to the neuron is launched
            neuron1 = Neuron(name='neurone1', parameters={'var1': 'val1'})
            params = {
                'param1':'parval1'
            }
            NeuronLauncher.start_neuron(neuron=neuron1,
                                        parameters_dict=params)
            mock_launch_neuron_method.assert_called_with(neuron1)
            mock_launch_neuron_method.reset_mock()

            # Assert the params are well passed to the neuron
            neuron2 = Neuron(name='neurone2', parameters={'var2': 'val2', 'args': ['arg1', 'arg2']})
            params = {
                'arg1':'argval1',
                'arg2':'argval2'
            }
            NeuronLauncher.start_neuron(neuron=neuron2,
                                        parameters_dict=params)
            neuron2_params = Neuron(name='neurone2',
                                    parameters={'var2': 'val2',
                                                'args': ['arg1', 'arg2'],
                                                'arg1':'argval1',
                                                'arg2':'argval2'}
                                    )
            mock_launch_neuron_method.assert_called_with(neuron2_params)
            mock_launch_neuron_method.reset_mock()

            # Assert the Neuron is not started when missing args
            neuron3 = Neuron(name='neurone3', parameters={'var3': 'val3', 'args': ['arg3', 'arg4']})
            params = {
                'arg1': 'argval1',
                'arg2': 'argval2'
            }
            NeuronLauncher.start_neuron(neuron=neuron3,
                                        parameters_dict=params)
            mock_launch_neuron_method.assert_not_called()
            mock_launch_neuron_method.reset_mock()

            # Assert no neuron is launched when waiting for args and none are given
            neuron4 = Neuron(name='neurone4', parameters={'var4': 'val4', 'args': ['arg5', 'arg6']})
            params = {}
            NeuronLauncher.start_neuron(neuron=neuron4,
                                        parameters_dict=params)
            mock_launch_neuron_method.assert_not_called()
            mock_launch_neuron_method.reset_mock()


