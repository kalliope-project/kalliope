import unittest

from core.ConfigurationManager import BrainLoader
from core.Models import Event
from core.Models import Neuron
from core.Models import Order


class TestBrainLoader(unittest.TestCase):

    def setUp(self):
        self.brain_to_test = "core/Tests/brains/brain_test.yml"
        self.expected_result = [
            {'signals': [{'order': 'test_order'}],
             'neurons': [{'say': {'message': ['test message']}}],
             'name': 'test'},
            {'signals': [{'order': 'test_order_2'}],
             'neurons': [{'say': {'message': ['test message']}}],
             'name': 'test2'},
            {'includes': ['included_brain_test.yml']},
            {'signals': [{'order': 'test_order_3'}],
             'neurons': [{'say': {'message': ['test message']}}],
             'name': 'test3'}
        ]

    # def test_get_yaml_config(self):
    #     """
    #     Test we can get a yaml config from the path
    #     """
    #     brain_loader = BrainLoader.Instance(file_path=self.brain_to_test)
    #     self.assertEqual(brain_loader.yaml_config, self.expected_result)
    #     del brain_loader
    #
    # def test_get_brain(self):
    #     """
    #     Test the class return a valid brain object
    #     """
    #
    #     neuron = Neuron(name='say', parameters={'message': ['test message']})
    #
    #     signal1 = Order(sentence="test_order")
    #     signal2 = Order(sentence="test_order_2")
    #     signal3 = Order(sentence="test_order_3")
    #
    #     synapse1 = Synapse(name="test", neurons=[neuron], signals=[signal1])
    #     synapse2 = Synapse(name="test2", neurons=[neuron], signals=[signal2])
    #     synapse3 = Synapse(name="test3", neurons=[neuron], signals=[signal3])
    #     synapses = [synapse1, synapse2, synapse3]
    #
    #     brain = Brain()
    #     brain.synapses = synapses
    #     brain.brain_file = self.brain_to_test
    #     brain.brain_yaml = self.expected_result
    #
    #     brain_loader = BrainLoader.Instance(file_path=self.brain_to_test)
    #     self.assertEqual(brain, brain_loader.brain)
    #     del brain_loader

    def test_get_neurons(self):
        neuron_list = [{'say': {'message': ['test message']}}]

        neuron = Neuron(name='say', parameters={'message': ['test message']})

        bl = BrainLoader.Instance(file_path=self.brain_to_test)
        neurons_from_brain_loader = bl._get_neurons(neuron_list)

        self.assertEqual([neuron], neurons_from_brain_loader)
        del bl

    def test_get_signals(self):
        signals = [{'order': 'test_order'}]

        signal = Order(sentence='test_order')

        bl = BrainLoader.Instance(file_path=self.brain_to_test)
        signals_from_brain_loader = bl._get_signals(signals)

        self.assertEqual([signal], signals_from_brain_loader)
        del bl

    def test_get_event_or_order_from_dict(self):

        order_object = Order(sentence="test_order")
        event_object = Event(period="0 7 * * *")

        dict_order = {'order': 'test_order'}
        dict_event = {'event': '0 7 * * *'}

        bl = BrainLoader.Instance(file_path=self.brain_to_test)
        order_from_bl = bl._get_event_or_order_from_dict(dict_order)
        event_from_bl = bl._get_event_or_order_from_dict(dict_event)

        self.assertEqual(order_from_bl, order_object)
        self.assertEqual(event_from_bl, event_object)
        del bl

    def test_singleton(self):
        bl1 = BrainLoader.Instance(file_path=self.brain_to_test)
        bl2 = BrainLoader.Instance(file_path=self.brain_to_test)

        self.assertTrue(bl1.brain is bl2.brain)
        del bl1
        del bl2

if __name__ == '__main__':
    unittest.main()
