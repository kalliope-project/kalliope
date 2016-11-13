import unittest

from core.ConfigurationManager import BrainLoader
from core.Models import Brain
from core.Models import Neuron
from core.Models import Order
from core.Models import Synapse


class TestBrainLoader(unittest.TestCase):

    def test_get_yaml_config(self):
        brain_to_test = "core/Tests/brains/brain_test.yml"
        expected_result = [
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

        self.assertEqual(BrainLoader.get_yaml_config(brain_to_test), expected_result)

    def test_get_brain(self):
        brain_to_test = "core/Tests/brains/brain_test.yml"

        neuron1 = Neuron(name='say', parameters={'message': 'test message'})
        neuron2 = Neuron(name='say', parameters={'message': 'test message'})
        neuron3 = Neuron(name='say', parameters={'message': 'test message'})

        signal1 = Order(sentence="test_order")
        signal2 = Order(sentence="test_order_2")
        signal3 = Order(sentence="test_order_3")

        synapse1 = Synapse(name="Synapse1", neurons=[neuron1], signals={signal1})
        synapse2 = Synapse(name="Synapse2", neurons=[neuron2], signals={signal2})
        synapse3 = Synapse(name="Synapse3", neurons=[neuron3], signals={signal3})
        synapses = [synapse1, synapse2, synapse3]

        expected_result = [
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

        brain = Brain()
        brain.synapses = synapses
        brain.brain_file = brain_to_test
        brain.brain_yaml = expected_result
        brain.is_loaded = False

        # TODO this is not working. how to test a singleton?
        self.assertEqual(brain, BrainLoader.get_brain(file_path=brain_to_test))



if __name__ == '__main__':
    unittest.main()
