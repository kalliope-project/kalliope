import unittest
import mock

from kalliope.core.Models.Resources import Resources
from kalliope.core.NeuronLauncher import NeuronLauncher, NeuronParameterNotAvailable
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
            # Assert to the neuron is launched with not parameter from order
            neuron1 = Neuron(name='neurone1', parameters={'var1': 'val1'})

            NeuronLauncher.start_neuron(neuron=neuron1)
            mock_launch_neuron_method.assert_called_with(neuron1)
            mock_launch_neuron_method.reset_mock()

            # Assert the params are well passed to the neuron
            neuron2 = Neuron(name='neurone2', parameters={'var2': 'val2', 'var3': "{{ var3 }}"})
            params = {
                'var3': 'value3'
            }
            NeuronLauncher.start_neuron(neuron=neuron2,
                                        parameters_dict=params)
            neuron2_params = Neuron(name='neurone2', parameters={'var2': 'val2', 'var3': 'value3'})

            mock_launch_neuron_method.assert_called_with(neuron2_params)
            mock_launch_neuron_method.reset_mock()

            # Assert the Neuron is not started when missing args
            neuron3 = Neuron(name='neurone3', parameters={'var3': 'val3', 'var4': '{{val4}}'})
            params = {
                'not_exist': 'test'
            }
            NeuronLauncher.start_neuron(neuron=neuron3,
                                        parameters_dict=params)
            mock_launch_neuron_method.assert_not_called()
            mock_launch_neuron_method.reset_mock()

            # Assert no neuron is launched when waiting for args and none are given
            neuron4 = Neuron(name='neurone4', parameters={'var5': 'val5', 'var6': '{{val6}}'})

            NeuronLauncher.start_neuron(neuron=neuron4)
            mock_launch_neuron_method.assert_not_called()
            mock_launch_neuron_method.reset_mock()

    def test_replace_brackets_by_loaded_parameter(self):
        # -------------------
        # test with string
        # -------------------
        # the target value to replace is present in the loaded parameter dict
        neuron_parameters = {
            "param1": "this is a value {{ replaced }}"
        }

        loaded_parameters = {
            "replaced": "replaced successfully"
        }

        expected_result = {
            "param1": "this is a value replaced successfully"
        }

        self.assertEqual(expected_result, NeuronLauncher._replace_brackets_by_loaded_parameter(neuron_parameters,
                                                                                               loaded_parameters))

        # the target value to replace is NOT present in the loaded parameter dict
        neuron_parameters = {
            "param1": "this is a value {{ replaced }}"
        }

        loaded_parameters = {
            "not_exist": "replaced successfully"
        }

        with self.assertRaises(NeuronParameterNotAvailable):
            NeuronLauncher._replace_brackets_by_loaded_parameter(neuron_parameters, loaded_parameters)

        # one parameter doesn't contains bracket, the other one do
        neuron_parameters = {
            "param1": "this is a value {{ replaced }}",
            "param2": "value"
        }

        loaded_parameters = {
            "replaced": "replaced successfully"
        }

        expected_result = {
            "param1": "this is a value replaced successfully",
            "param2": "value"
        }

        self.assertEqual(expected_result, NeuronLauncher._replace_brackets_by_loaded_parameter(neuron_parameters,
                                                                                               loaded_parameters))

        # parameters are integer or boolean
        neuron_parameters = {
            "param1": 1,
            "param2": True
        }

        loaded_parameters = {
            "replaced": "replaced successfully"
        }

        expected_result = {
            "param1": 1,
            "param2": True
        }

        self.assertEqual(expected_result, NeuronLauncher._replace_brackets_by_loaded_parameter(neuron_parameters,
                                                                                               loaded_parameters))

        # parameters are say_template or file template. Should not be altered by the loader
        neuron_parameters = {
            "say_template": "{{output}}",
            "file_template": "here is a file"
        }

        loaded_parameters = {
            "output": "should not be used"
        }

        expected_result = {
            "say_template": "{{output}}",
            "file_template": "here is a file"
        }

        self.assertEqual(expected_result, NeuronLauncher._replace_brackets_by_loaded_parameter(neuron_parameters,
                                                                                               loaded_parameters))

    def test_parameters_are_available_in_loaded_parameters(self):
        # the parameter in bracket is available in the dict
        string_parameters = "this is a {{ parameter1 }}"
        loaded_parameters = {"parameter1": "value"}

        self.assertTrue(NeuronLauncher._neuron_parameters_are_available_in_loaded_parameters(string_parameters,
                                                                                            loaded_parameters))

        # the parameter in bracket is NOT available in the dict
        string_parameters = "this is a {{ parameter1 }}"
        loaded_parameters = {"parameter2": "value"}

        self.assertFalse(NeuronLauncher._neuron_parameters_are_available_in_loaded_parameters(string_parameters,
                                                                                             loaded_parameters))

        # the string_parameters doesn't contains bracket in bracket is available in the dict
        string_parameters = "this is a {{ parameter1 }}"
        loaded_parameters = {"parameter1": "value"}

        self.assertTrue(NeuronLauncher._neuron_parameters_are_available_in_loaded_parameters(string_parameters,
                                                                                            loaded_parameters))

        # the string_parameters contains 2 parameters available in the dict
        string_parameters = "this is a {{ parameter1 }} and this is {{ parameter2 }}"
        loaded_parameters = {"parameter1": "value", "parameter2": "other value"}

        self.assertTrue(NeuronLauncher._neuron_parameters_are_available_in_loaded_parameters(string_parameters,
                                                                                            loaded_parameters))

        # the string_parameters contains 2 parameters and one of them is not available in the dict
        string_parameters = "this is a {{ parameter1 }} and this is {{ parameter2 }}"
        loaded_parameters = {"parameter1": "value", "parameter3": "other value"}

        self.assertFalse(NeuronLauncher._neuron_parameters_are_available_in_loaded_parameters(string_parameters,
                                                                                             loaded_parameters))


if __name__ == '__main__':
    unittest.main()

    # suite = unittest.TestSuite()
    # suite.addTest(TestNeuronLauncher("test_start_neuron"))
    # runner = unittest.TextTestRunner()
    # runner.run(suite)
