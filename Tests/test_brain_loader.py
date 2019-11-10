# coding: utf8
import os
import unittest

from Tests.utils.utils import get_test_path
from kalliope.core.Models import Singleton, Signal

from kalliope.core.ConfigurationManager import BrainLoader
from kalliope.core.Models import Neuron
from kalliope.core.Models import Synapse
from kalliope.core.Models.Brain import Brain
from kalliope.core.Models.settings.Settings import Settings


class TestBrainLoader(unittest.TestCase):

    def setUp(self):
        # be sure the brain haven't been instantiated before
        Singleton._instances = dict()
        self.brain_to_test = get_test_path("brains/brain_test.yml")

        self.expected_result = [
            {'signals': [{'order': 'test_order'}],
             'neurons': [{'say': {'message': ['test message']}}],
             'name': 'test'},
            {'signals': [{'order': 'test_order_2'}],
             'neurons': [{'say': {'message': ['test message']}}],
             'name': 'test2'},
            {'signals': [{'order': 'order_for_int'}],
             'neurons': [{'sleep': {'seconds': 60}}],
             'name': 'testint'},
            {'includes': ['included_brain_test.yml']},
            {'signals': [{'order': 'test_order_3'}],
             'neurons': [{'say': {'message': ['test message']}}],
             'name': 'test3'}
        ]

    def tearDown(self):
        Singleton._instances = dict()

    def test_get_yaml_config(self):
        """
        Test we can get a yaml config from the path
        """
        brain_loader = BrainLoader(file_path=self.brain_to_test)
        self.assertEqual(brain_loader.yaml_config, self.expected_result)

    def test_load_brain(self):
        """
        Test the class return a valid brain object
        """

        neuron = Neuron(name='say', parameters={'message': ['test message']})
        neuron2 = Neuron(name='sleep', parameters={'seconds': 60})

        signal1 = Signal(name="order", parameters="test_order")
        signal2 = Signal(name="order", parameters="test_order_2")
        signal3 = Signal(name="order", parameters="test_order_3")
        signal4 = Signal(name="order", parameters="order_for_int")

        synapse1 = Synapse(name="test", neurons=[neuron], signals=[signal1])
        synapse2 = Synapse(name="test2", neurons=[neuron], signals=[signal2])
        synapse3 = Synapse(name="test3", neurons=[neuron], signals=[signal3])
        synapse4 = Synapse(name="testint", neurons=[neuron2], signals=[signal4])
        synapses = [synapse1, synapse2, synapse4, synapse3]

        brain = Brain()
        brain.synapses = synapses
        brain.brain_file = self.brain_to_test
        brain.brain_yaml = self.expected_result

        brain_loader = BrainLoader(file_path=self.brain_to_test)
        self.assertEqual(brain, brain_loader.brain)

    def test_get_neurons(self):
        """
        Test to get neurons from the brainLoader
        scenarii:
            - 1/ get a simple neuron from the brainloader
            - 2/ get a neuron with brackets
            - 3/ get a neuron with int as parameters
        """
        # 1/ get a simple neuron from the brainloader
        st = Settings()
        neuron_list = [{'say': {'message': ['test message']}}]

        neuron = Neuron(name='say', parameters={'message': ['test message']})

        bl = BrainLoader(file_path=self.brain_to_test)
        neurons_from_brain_loader = bl.get_neurons(neuron_list,
                                                   settings=st)

        self.assertEqual([neuron], neurons_from_brain_loader)

        # 2/ get a neuron with global variables as parameters
        neuron_list = [{'say': {'message': ['bonjour {{name}}']}}]

        st = Settings()
        bl = BrainLoader(file_path=self.brain_to_test)
        neurons_from_brain_loader = bl.get_neurons(neuron_list,
                                                   settings=st)

        neuron = Neuron(name='say', parameters={'message': ['bonjour {{name}}']})

        self.assertEqual([neuron], neurons_from_brain_loader)

        # 3/ get a neuron with int as parameters
        st = Settings()
        neuron_list = [{'sleep': {'seconds': 60}}]

        neuron = Neuron(name='sleep', parameters={'seconds': 60})

        bl = BrainLoader(file_path=self.brain_to_test)
        neurons_from_brain_loader = bl.get_neurons(neuron_list,
                                                   settings=st)

        self.assertEqual([neuron], neurons_from_brain_loader)

    def test_get_signals(self):
        signals = [{'order': 'test_order'}]

        signal = Signal(name="order", parameters="test_order")

        bl = BrainLoader(file_path=self.brain_to_test)
        signals_from_brain_loader = bl.get_signals(signals)

        self.assertEqual([signal], signals_from_brain_loader)

    def test_singleton(self):
        bl1 = BrainLoader(file_path=self.brain_to_test)
        bl2 = BrainLoader(file_path=self.brain_to_test)

        self.assertTrue(bl1.brain is bl2.brain)


if __name__ == '__main__':
    unittest.main()
