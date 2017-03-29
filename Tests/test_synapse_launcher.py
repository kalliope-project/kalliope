import unittest

import mock

from kalliope.core.Models import Brain
from kalliope.core.Models.Settings import Settings
from kalliope.core.SynapseLauncher import SynapseLauncher, SynapseNameNotFound

from kalliope.core.Models import Neuron
from kalliope.core.Models import Order
from kalliope.core.Models import Synapse


class TestSynapseLauncher(unittest.TestCase):
    """
    Test the class SynapseLauncher
    """

    def setUp(self):
        # Init
        neuron1 = Neuron(name='neurone1', parameters={'var1': 'val1'})
        neuron2 = Neuron(name='neurone2', parameters={'var2': 'val2'})
        neuron3 = Neuron(name='neurone3', parameters={'var3': 'val3'})
        neuron4 = Neuron(name='neurone4', parameters={'var4': 'val4'})

        signal1 = Order(sentence="this is the sentence")
        signal2 = Order(sentence="this is the second sentence")
        signal3 = Order(sentence="that is part of the third sentence")

        self.synapse1 = Synapse(name="Synapse1", neurons=[neuron1, neuron2], signals=[signal1])
        self.synapse2 = Synapse(name="Synapse2", neurons=[neuron3, neuron4], signals=[signal2])
        self.synapse3 = Synapse(name="Synapse3", neurons=[neuron2, neuron4], signals=[signal3])

        all_synapse_list = [self.synapse1,
                            self.synapse2,
                            self.synapse3]

        self.brain_test = Brain(synapses=all_synapse_list)
        self.settings_test = Settings(default_synapse="Synapse3")

    def test_run_matching_synapse_or_default(self):

        # test_match_synapse1
        with mock.patch("kalliope.core.NeuronLauncher.start_neuron_list"):
            order_to_match = "this is the sentence"
            expected_result = [self.synapse1]

            self.assertEqual(expected_result,
                             SynapseLauncher.run_matching_synapse_or_default(order_to_match,
                                                                             brain=self.brain_test,
                                                                             settings=self.settings_test))

        # test_match_synapse1_and_2
        with mock.patch("kalliope.core.NeuronLauncher.start_neuron_list"):
            order_to_match = "this is the second sentence"
            expected_result = [self.synapse1, self.synapse2]

            self.assertEqual(expected_result,
                             SynapseLauncher.run_matching_synapse_or_default(order_to_match,
                                                                             brain=self.brain_test,
                                                                             settings=self.settings_test))

        # test_match_default_synapse
        with mock.patch("kalliope.core.NeuronLauncher.start_neuron"):
            order_to_match = "this is an invalid order"
            expected_result = [self.synapse3]

            self.assertEqual(expected_result,
                             SynapseLauncher.run_matching_synapse_or_default(order_to_match,
                                                                             brain=self.brain_test,
                                                                             settings=self.settings_test))

    def test_start_synapse(self):
        with mock.patch("kalliope.core.NeuronLauncher.start_neuron"):
            expected_result = self.synapse1
            self.assertEqual(expected_result,
                             SynapseLauncher.start_synapse("Synapse1", brain=self.brain_test))

        with self.assertRaises(SynapseNameNotFound):
            SynapseLauncher.start_synapse(name="no_do_exist", brain=self.brain_test)
