import unittest

import logging

from kalliope.core.Models import Brain
from kalliope.core.Models import Neuron
from kalliope.core.Models import Order
from kalliope.core.Models import Synapse
from kalliope.core.Models.Settings import Settings
from kalliope.core.OrderAnalyser2 import OrderAnalyser2


logging.basicConfig()
logger = logging.getLogger("kalliope")
logger.setLevel(logging.DEBUG)


class TestOrderAnalyser2(unittest.TestCase):

    """Test case for the OrderAnalyser Class"""

    def setUp(self):
        pass

    def test_get_matching_synapse(self):
        # Init
        neuron1 = Neuron(name='neurone1', parameters={'var1': 'val1'})
        neuron2 = Neuron(name='neurone2', parameters={'var2': 'val2'})
        neuron3 = Neuron(name='neurone3', parameters={'var3': 'val3'})
        neuron4 = Neuron(name='neurone4', parameters={'var4': 'val4'})

        signal1 = Order(sentence="this is the sentence")
        signal2 = Order(sentence="this is the second sentence")
        signal3 = Order(sentence="that is part of the third sentence")

        synapse1 = Synapse(name="Synapse1", neurons=[neuron1, neuron2], signals=[signal1])
        synapse2 = Synapse(name="Synapse2", neurons=[neuron3, neuron4], signals=[signal2])
        synapse3 = Synapse(name="Synapse3", neurons=[neuron2, neuron4], signals=[signal3])

        all_synapse_list = [synapse1,
                            synapse2,
                            synapse3]

        br = Brain(synapses=all_synapse_list)

        # TEST1: should return synapse1
        spoken_order = "this is the sentence"
        matched_synapses = OrderAnalyser2.get_matching_synapse(order=spoken_order, brain=br)
        self.assertEqual(len(matched_synapses), 1)
        self.assertTrue(any(synapse1 in matched_synapse for matched_synapse in matched_synapses))

        # TEST2: should return synapse1 and 2
        spoken_order = "this is the second sentence"
        matched_synapses = OrderAnalyser2.get_matching_synapse(order=spoken_order, brain=br)
        self.assertEqual(len(matched_synapses), 2)
        self.assertTrue(synapse1, synapse2 in matched_synapses)

        # TEST3: should empty
        spoken_order = "not a valid order"
        matched_synapses = OrderAnalyser2.get_matching_synapse(order=spoken_order, brain=br)
        self.assertFalse(matched_synapses)

    def test_spelt_order_match_brain_order_via_table(self):
        order_to_test = "this is the order"
        sentence_to_test = "this is the order"

        # Success
        self.assertTrue(OrderAnalyser2.spelt_order_match_brain_order_via_table(order_to_test, sentence_to_test))

        # Failure
        sentence_to_test = "unexpected sentence"
        self.assertFalse(OrderAnalyser2.spelt_order_match_brain_order_via_table(order_to_test, sentence_to_test))

        # Upper/lower cases
        sentence_to_test = "THIS is THE order"
        self.assertTrue(OrderAnalyser2.spelt_order_match_brain_order_via_table(order_to_test, sentence_to_test))

    def test_get_split_order_without_bracket(self):
        # Success
        order_to_test = "this is the order"
        expected_result = ["this", "is", "the", "order"]
        self.assertEqual(OrderAnalyser2._get_split_order_without_bracket(order_to_test), expected_result,
                         "No brackets Fails to return the expected list")

        order_to_test = "this is the {{ order }}"
        expected_result = ["this", "is", "the"]
        self.assertEqual(OrderAnalyser2._get_split_order_without_bracket(order_to_test), expected_result,
                         "With spaced brackets Fails to return the expected list")

        order_to_test = "this is the {{order }}"    # left bracket without space
        expected_result = ["this", "is", "the"]
        self.assertEqual(OrderAnalyser2._get_split_order_without_bracket(order_to_test), expected_result,
                         "Left brackets Fails to return the expected list")

        order_to_test = "this is the {{ order}}"    # right bracket without space
        expected_result = ["this", "is", "the"]
        self.assertEqual(OrderAnalyser2._get_split_order_without_bracket(order_to_test), expected_result,
                         "Right brackets Fails to return the expected list")

        order_to_test = "this is the {{order}}"  # bracket without space
        expected_result = ["this", "is", "the"]
        self.assertEqual(OrderAnalyser2._get_split_order_without_bracket(order_to_test), expected_result,
                         "No space brackets Fails to return the expected list")

    def test_counter_subset(self):
        list1 = ("word1", "word2")
        list2 = ("word3", "word4")
        list3 = ("word1", "word2", "word3", "word4")

        self.assertFalse(OrderAnalyser2._counter_subset(list1, list2))
        self.assertTrue(OrderAnalyser2._counter_subset(list1, list3))
        self.assertTrue(OrderAnalyser2._counter_subset(list2, list3))


if __name__ == '__main__':
    unittest.main()
