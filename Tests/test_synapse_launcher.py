import unittest

import mock

from kalliope.core import LIFOBuffer
from kalliope.core.Models import Brain
from kalliope.core.Models.MatchedSynapse import MatchedSynapse
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

        self.all_synapse_list = [self.synapse1,
                                 self.synapse2,
                                 self.synapse3]

        self.brain_test = Brain(synapses=self.all_synapse_list)
        self.settings_test = Settings(default_synapse="Synapse3")

        # clean the LiFO
        LIFOBuffer.lifo_list = list()

    def test_start_synapse_by_name(self):
        # existing synapse in the brain
        with mock.patch("kalliope.core.LIFOBuffer.execute"):
            should_be_created_matched_synapse = MatchedSynapse(matched_synapse=self.synapse1)
            SynapseLauncher.start_synapse_by_name("Synapse1", brain=self.brain_test)
            # we expect that the lifo has been loaded with the synapse to run
            expected_result = [[should_be_created_matched_synapse]]
            self.assertEqual(expected_result, LIFOBuffer.lifo_list)

        # non existing synapse in the brain
        with self.assertRaises(SynapseNameNotFound):
            SynapseLauncher.start_synapse_by_name("not_existing", brain=self.brain_test)

    def test_run_matching_synapse_from_order(self):
        # ------------------
        # test_match_synapse1
        # ------------------
        with mock.patch("kalliope.core.LIFOBuffer.execute"):
            order_to_match = "this is the sentence"

            should_be_created_matched_synapse = MatchedSynapse(matched_synapse=self.synapse1,
                                                               user_order=order_to_match,
                                                               matched_order="this is the sentence")
            expected_result = [[should_be_created_matched_synapse]]
            SynapseLauncher.run_matching_synapse_from_order(order_to_match,
                                                            brain=self.brain_test,
                                                            settings=self.settings_test)

            self.assertEqual(expected_result, LIFOBuffer.lifo_list)

        # -------------------------
        # test_match_synapse1_and_2
        # -------------------------
        # clean LIFO
        LIFOBuffer.lifo_list = list()
        with mock.patch("kalliope.core.LIFOBuffer.execute"):
            order_to_match = "this is the second sentence"
            should_be_created_matched_synapse1 = MatchedSynapse(matched_synapse=self.synapse1,
                                                                user_order=order_to_match,
                                                                matched_order="this is the sentence")
            should_be_created_matched_synapse2 = MatchedSynapse(matched_synapse=self.synapse2,
                                                                user_order=order_to_match,
                                                                matched_order="this is the second sentence")

            expected_result = [[should_be_created_matched_synapse1, should_be_created_matched_synapse2]]
            SynapseLauncher.run_matching_synapse_from_order(order_to_match,
                                                            brain=self.brain_test,
                                                            settings=self.settings_test)
            self.assertEqual(expected_result, LIFOBuffer.lifo_list)

        # -------------------------
        # test_match_default_synapse
        # -------------------------
        # clean LIFO
        LIFOBuffer.lifo_list = list()
        with mock.patch("kalliope.core.LIFOBuffer.execute"):
            order_to_match = "not existing sentence"
            should_be_created_matched_synapse = MatchedSynapse(matched_synapse=self.synapse3,
                                                               user_order=order_to_match,
                                                               matched_order=None)

            expected_result = [[should_be_created_matched_synapse]]
            SynapseLauncher.run_matching_synapse_from_order(order_to_match,
                                                            brain=self.brain_test,
                                                            settings=self.settings_test)
            self.assertEqual(expected_result, LIFOBuffer.lifo_list)

        # -------------------------
        # test_no_match_and_no_default_synapse
        # -------------------------
        # clean LIFO
        LIFOBuffer.lifo_list = list()
        with mock.patch("kalliope.core.LIFOBuffer.execute"):
            order_to_match = "not existing sentence"
            new_settings = Settings()
            expected_result = [[]]
            SynapseLauncher.run_matching_synapse_from_order(order_to_match,
                                                            brain=self.brain_test,
                                                            settings=new_settings)
            self.assertEqual(expected_result, LIFOBuffer.lifo_list)
