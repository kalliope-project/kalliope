import unittest

from kalliope.core.ConfigurationManager.ConfigurationChecker import ConfigurationChecker, NoSynapeName, \
                                                NoSynapeNeurons, NoSynapeSignals, NoValidSignal, MultipleSameSynapseName
from kalliope.core.Models import Synapse
from kalliope.core.Utils.Utils import KalliopeModuleNotFoundError


class TestConfigurationChecker(unittest.TestCase):
    """
    Class used to test the ConfigurationChecker class
    """

    def setUp(self):
        pass

    def test_check_synape_dict(self):
        valid_synapse_dict = {
            'signals': [{'order': 'test_order'}],
            'neurons': [{'say': {'message': ['test message']}}],
            'name': 'test'
        }

        synapse_dict_without_name = {
            'signals': [{'order': 'test_order'}],
            'neurons': [{'say': {'message': ['test message']}}]
        }

        synapse_dict_without_neurons = {
            'signals': [{'order': 'test_order'}],
            'name': 'test'
        }

        synapse_dict_without_signals = {
            'neurons': [{'say': {'message': ['test message']}}],
            'name': 'test'
        }

        self.assertTrue(ConfigurationChecker.check_synape_dict(valid_synapse_dict))

        with self.assertRaises(NoSynapeName):
            ConfigurationChecker.check_synape_dict(synapse_dict_without_name)

        with self.assertRaises(NoSynapeNeurons):
            ConfigurationChecker.check_synape_dict(synapse_dict_without_neurons)

        with self.assertRaises(NoSynapeSignals):
            ConfigurationChecker.check_synape_dict(synapse_dict_without_signals)

    def test_check_neuron_dict(self):
        valid_neuron = {'say': {'message': ['test message']}}
        invalid_neuron = {'not_existing_neuron': {'message': ['test message']}}

        self.assertTrue(ConfigurationChecker.check_neuron_dict(valid_neuron))

        with self.assertRaises(KalliopeModuleNotFoundError):
            ConfigurationChecker.check_neuron_dict(invalid_neuron)

    def test_check_signal_dict(self):
        valid_signal = {'event': {'parameter_1': ['value1']}}
        invalid_signal = {'non_existing_signal_name': {'parameter_2': ['value2']}}

        self.assertTrue(ConfigurationChecker.check_signal_dict(valid_signal))

        with self.assertRaises(KalliopeModuleNotFoundError):
            ConfigurationChecker.check_signal_dict(invalid_signal)

    def test_check_synapes(self):
        synapse_1 = Synapse(name="test")
        synapse_2 = Synapse(name="test2")
        synapse_3 = Synapse(name="test")

        valid_synapse_list = [synapse_1, synapse_2]
        invalid_synapse_list = [synapse_1, synapse_3]

        self.assertTrue(ConfigurationChecker.check_synapes(valid_synapse_list))

        with self.assertRaises(MultipleSameSynapseName):
            ConfigurationChecker.check_synapes(invalid_synapse_list)


if __name__ == '__main__':
    unittest.main()
