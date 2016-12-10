import unittest

from kalliope.core.ConfigurationManager.ConfigurationChecker import ConfigurationChecker, NoSynapeName, NoSynapeNeurons, \
    NoSynapeSignals, NoValidSignal, NoEventPeriod, NoValidOrder, MultipleSameSynapseName
from kalliope.core.Models import Synapse
from kalliope.core.Utils.Utils import ModuleNotFoundError


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

        with self.assertRaises(ModuleNotFoundError):
            ConfigurationChecker.check_neuron_dict(invalid_neuron)

    def test_check_signal_dict(self):
        valid_signal_with_order = {'order': 'test_order'}
        valid_signal_with_event = {'event': '0 * * * *'}
        invalid_signal = {'invalid_option': 'test_order'}

        self.assertTrue(ConfigurationChecker.check_signal_dict(valid_signal_with_order))
        self.assertTrue(ConfigurationChecker.check_signal_dict(valid_signal_with_event))

        with self.assertRaises(NoValidSignal):
            ConfigurationChecker.check_signal_dict(invalid_signal)

    def test_check_event_dict(self):
        valid_event = {
            "hour": "18",
            "minute": "16"
          }
        invalid_event = None
        invalid_event2 = ""
        invalid_event3 = {
            "notexisting": "12"
        }

        self.assertTrue(ConfigurationChecker.check_event_dict(valid_event))

        with self.assertRaises(NoEventPeriod):
            ConfigurationChecker.check_event_dict(invalid_event)
        with self.assertRaises(NoEventPeriod):
            ConfigurationChecker.check_event_dict(invalid_event2)
        with self.assertRaises(NoEventPeriod):
            ConfigurationChecker.check_event_dict(invalid_event3)

    def test_check_order_dict(self):
        valid_order = 'test_order'
        invalid_order = ''
        invalid_order2 = None

        self.assertTrue(ConfigurationChecker.check_order_dict(valid_order))

        with self.assertRaises(NoValidOrder):
            ConfigurationChecker.check_order_dict(invalid_order)
        with self.assertRaises(NoValidOrder):
            ConfigurationChecker.check_order_dict(invalid_order2)

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
