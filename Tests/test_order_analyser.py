import unittest


from kalliope.core.Models import Brain
from kalliope.core.Models import Neuron
from kalliope.core.Models import Synapse
from kalliope.core.Models.MatchedSynapse import MatchedSynapse
from kalliope.core.Models.Signal import Signal
from kalliope.core.OrderAnalyser import OrderAnalyser


class TestOrderAnalyser(unittest.TestCase):

    """Test case for the OrderAnalyser Class"""

    def setUp(self):
        pass

    def test_get_matching_synapse(self):
        # Init
        neuron1 = Neuron(name='neurone1', parameters={'var1': 'val1'})
        neuron2 = Neuron(name='neurone2', parameters={'var2': 'val2'})
        neuron3 = Neuron(name='neurone3', parameters={'var3': 'val3'})
        neuron4 = Neuron(name='neurone4', parameters={'var4': 'val4'})

        signal1 = Signal(name="order", parameters="this is the sentence")
        signal2 = Signal(name="order", parameters="this is the second sentence")
        signal3 = Signal(name="order", parameters="that is part of the third sentence")
        signal4 = Signal(name="order", parameters={"matching-type": "strict",
                                                   "text": "that is part of the fourth sentence"})
        signal5 = Signal(name="order", parameters={"matching-type": "ordered-strict",
                                                   "text": "sentence 5 with specific order"})
        signal6 = Signal(name="order", parameters={"matching-type": "normal",
                                                   "text": "matching type normal"})
        signal7 = Signal(name="order", parameters={"matching-type": "non-existing",
                                                   "text": "matching type non existing"})
        signal8 = Signal(name="order", parameters={"matching-type": "non-existing",
                                                   "non-existing-parameter": "will not match order"})

        synapse1 = Synapse(name="Synapse1", neurons=[neuron1, neuron2], signals=[signal1])
        synapse2 = Synapse(name="Synapse2", neurons=[neuron3, neuron4], signals=[signal2])
        synapse3 = Synapse(name="Synapse3", neurons=[neuron2, neuron4], signals=[signal3])
        synapse4 = Synapse(name="Synapse4", neurons=[neuron2, neuron4], signals=[signal4])
        synapse5 = Synapse(name="Synapse5", neurons=[neuron1, neuron2], signals=[signal5])
        synapse6 = Synapse(name="Synapse6", neurons=[neuron1, neuron2], signals=[signal6])
        synapse7 = Synapse(name="Synapse6", neurons=[neuron1, neuron2], signals=[signal7])
        synapse8 = Synapse(name="Synapse6", neurons=[neuron1, neuron2], signals=[signal8])

        all_synapse_list = [synapse1,
                            synapse2,
                            synapse3,
                            synapse4,
                            synapse5,
                            synapse6,
                            synapse7,
                            synapse8]

        br = Brain(synapses=all_synapse_list)

        # TEST1: should return synapse1
        spoken_order = "this is the sentence"

        # Create the matched synapse
        expected_matched_synapse_1 = MatchedSynapse(matched_synapse=synapse1,
                                                    matched_order=spoken_order,
                                                    user_order=spoken_order)

        matched_synapses = OrderAnalyser.get_matching_synapse(order=spoken_order, brain=br)
        self.assertEqual(len(matched_synapses), 1)
        self.assertTrue(expected_matched_synapse_1 in matched_synapses)

        # with defined normal matching type
        spoken_order = "matching type normal"
        expected_matched_synapse_5 = MatchedSynapse(matched_synapse=synapse6,
                                                    matched_order=spoken_order,
                                                    user_order=spoken_order)

        matched_synapses = OrderAnalyser.get_matching_synapse(order=spoken_order, brain=br)
        self.assertEqual(len(matched_synapses), 1)
        self.assertTrue(expected_matched_synapse_5 in matched_synapses)

        # TEST2: should return synapse1 and 2
        spoken_order = "this is the second sentence"
        expected_matched_synapse_2 = MatchedSynapse(matched_synapse=synapse1,
                                                    matched_order=spoken_order,
                                                    user_order=spoken_order)
        matched_synapses = OrderAnalyser.get_matching_synapse(order=spoken_order, brain=br)
        self.assertEqual(len(matched_synapses), 2)
        self.assertTrue(expected_matched_synapse_1, expected_matched_synapse_2 in matched_synapses)

        # TEST3: should empty
        spoken_order = "not a valid order"
        matched_synapses = OrderAnalyser.get_matching_synapse(order=spoken_order, brain=br)
        self.assertFalse(matched_synapses)

        # TEST4: with matching type strict
        spoken_order = "that is part of the fourth sentence"
        expected_matched_synapse_3 = MatchedSynapse(matched_synapse=synapse4,
                                                    matched_order=spoken_order,
                                                    user_order=spoken_order)
        matched_synapses = OrderAnalyser.get_matching_synapse(order=spoken_order, brain=br)
        self.assertTrue(expected_matched_synapse_3 in matched_synapses)

        spoken_order = "that is part of the fourth sentence with more word"
        matched_synapses = OrderAnalyser.get_matching_synapse(order=spoken_order, brain=br)
        self.assertFalse(matched_synapses)

        # TEST5: with matching type ordered strict
        spoken_order = "sentence 5 with specific order"
        expected_matched_synapse_4 = MatchedSynapse(matched_synapse=synapse5,
                                                    matched_order=spoken_order,
                                                    user_order=spoken_order)
        matched_synapses = OrderAnalyser.get_matching_synapse(order=spoken_order, brain=br)
        self.assertEqual(len(matched_synapses), 1)
        self.assertTrue(expected_matched_synapse_4 in matched_synapses)

        spoken_order = "order specific with 5 sentence"
        matched_synapses = OrderAnalyser.get_matching_synapse(order=spoken_order, brain=br)
        self.assertFalse(matched_synapses)

        # TEST6: non supported type of matching. should fallback to normal
        spoken_order = "matching type non existing"
        expected_matched_synapse_5 = MatchedSynapse(matched_synapse=synapse7,
                                                    matched_order=spoken_order,
                                                    user_order=spoken_order)
        matched_synapses = OrderAnalyser.get_matching_synapse(order=spoken_order, brain=br)
        self.assertTrue(expected_matched_synapse_5 in matched_synapses)

    def test_get_split_order_without_bracket(self):
        # Success
        order_to_test = "this is the order"
        expected_result = ["this", "is", "the", "order"]
        self.assertEqual(OrderAnalyser._get_split_order_without_bracket(order_to_test), expected_result,
                         "No brackets Fails to return the expected list")

        order_to_test = "this is the {{ order }}"
        expected_result = ["this", "is", "the"]
        self.assertEqual(OrderAnalyser._get_split_order_without_bracket(order_to_test), expected_result,
                         "With spaced brackets Fails to return the expected list")

        order_to_test = "this is the {{order }}"    # left bracket without space
        expected_result = ["this", "is", "the"]
        self.assertEqual(OrderAnalyser._get_split_order_without_bracket(order_to_test), expected_result,
                         "Left brackets Fails to return the expected list")

        order_to_test = "this is the {{ order}}"    # right bracket without space
        expected_result = ["this", "is", "the"]
        self.assertEqual(OrderAnalyser._get_split_order_without_bracket(order_to_test), expected_result,
                         "Right brackets Fails to return the expected list")

        order_to_test = "this is the {{order}}"  # bracket without space
        expected_result = ["this", "is", "the"]
        self.assertEqual(OrderAnalyser._get_split_order_without_bracket(order_to_test), expected_result,
                         "No space brackets Fails to return the expected list")

    def test_is_normal_matching(self):
        # same order
        test_order = "expected order in the signal"
        test_signal = "expected order in the signal"

        self.assertTrue(OrderAnalyser.is_normal_matching(user_order=test_order,
                                                         signal_order=test_signal))

        # not the same order
        test_order = "this is an order"
        test_signal = "expected order in the signal"

        self.assertFalse(OrderAnalyser.is_normal_matching(user_order=test_order,
                                                          signal_order=test_signal))

        # same order with more word in the user order
        test_order = "expected order in the signal with more word"
        test_signal = "expected order in the signal"

        self.assertTrue(OrderAnalyser.is_normal_matching(user_order=test_order,
                                                         signal_order=test_signal))

        # same order with bracket
        test_order = "expected order in the signal"
        test_signal = "expected order in the signal {{ variable }}"

        self.assertTrue(OrderAnalyser.is_normal_matching(user_order=test_order,
                                                         signal_order=test_signal))

        # same order with bracket
        test_order = "expected order in the signal variable_to_catch"
        test_signal = "expected order in the signal {{ variable }}"

        self.assertTrue(OrderAnalyser.is_normal_matching(user_order=test_order,
                                                         signal_order=test_signal))

        # same order with bracket and words after brackets
        test_order = "expected order in the signal variable_to_catch other word"
        test_signal = "expected order in the signal {{ variable }} other word"

        self.assertTrue(OrderAnalyser.is_normal_matching(user_order=test_order,
                                                         signal_order=test_signal))

    def test_is_strict_matching(self):
        # same order with same amount of word
        test_order = "expected order in the signal"
        test_signal = "expected order in the signal"

        self.assertTrue(OrderAnalyser.is_strict_matching(user_order=test_order,
                                                         signal_order=test_signal))

        # same order but not the same amount of word
        test_order = "expected order in the signal with more word"
        test_signal = "expected order in the signal"

        self.assertFalse(OrderAnalyser.is_strict_matching(user_order=test_order,
                                                          signal_order=test_signal))

        # same order with same amount of word and brackets
        test_order = "expected order in the signal variable_to_catch"
        test_signal = "expected order in the signal {{ variable }}"

        self.assertTrue(OrderAnalyser.is_strict_matching(user_order=test_order,
                                                         signal_order=test_signal))

        # same order with same amount of word and brackets with words after last brackets
        test_order = "expected order in the signal variable_to_catch other word"
        test_signal = "expected order in the signal {{ variable }} other word"

        self.assertTrue(OrderAnalyser.is_strict_matching(user_order=test_order,
                                                         signal_order=test_signal))

        # same order with same amount of word and brackets with words after last brackets but more words
        test_order = "expected order in the signal variable_to_catch other word and more word"
        test_signal = "expected order in the signal {{ variable }} other word"

        self.assertFalse(OrderAnalyser.is_strict_matching(user_order=test_order,
                                                          signal_order=test_signal))

    def test_ordered_strict_matching(self):
        # same order with same amount of word with same order
        test_order = "expected order in the signal"
        test_signal = "expected order in the signal"
        self.assertTrue(OrderAnalyser.is_ordered_strict_matching(user_order=test_order,
                                                                 signal_order=test_signal))

        # same order with same amount of word without same order
        test_order = "signal the in order expected"
        test_signal = "expected order in the signal"
        self.assertFalse(OrderAnalyser.is_ordered_strict_matching(user_order=test_order,
                                                                  signal_order=test_signal))

        # same order with same amount of word and brackets in the same order
        test_order = "expected order in the signal variable_to_catch"
        test_signal = "expected order in the signal {{ variable }}"

        self.assertTrue(OrderAnalyser.is_ordered_strict_matching(user_order=test_order,
                                                                 signal_order=test_signal))

        # same order with same amount of word and brackets in the same order with words after bracket
        test_order = "expected order in the signal variable_to_catch with word"
        test_signal = "expected order in the signal {{ variable }} with word"

        self.assertTrue(OrderAnalyser.is_ordered_strict_matching(user_order=test_order,
                                                                 signal_order=test_signal))

        # not same order with same amount of word and brackets
        test_order = "signal the in order expected"
        test_signal = "expected order in the signal {{ variable }}"
        self.assertFalse(OrderAnalyser.is_ordered_strict_matching(user_order=test_order,
                                                                  signal_order=test_signal))

        # not same order with same amount of word and brackets with words after bracket
        test_order = "word expected order in the signal variable_to_catch with"
        test_signal = "expected order in the signal {{ variable }} with word"

        self.assertFalse(OrderAnalyser.is_ordered_strict_matching(user_order=test_order,
                                                                  signal_order=test_signal))

    def test_is_order_matching(self):
        # all lowercase
        test_order = "expected order in the signal"
        test_signal = "expected order in the signal"
        self.assertTrue(OrderAnalyser.is_order_matching(user_order=test_order,
                                                        signal_order=test_signal))

        # with uppercase
        test_order = "Expected Order In The Signal"
        test_signal = "expected order in the signal"
        self.assertTrue(OrderAnalyser.is_order_matching(user_order=test_order,
                                                        signal_order=test_signal))


if __name__ == '__main__':
    unittest.main()

    # suite = unittest.TestSuite()
    # suite.addTest(TestOrderAnalyser("test_get_matching_synapse"))
    # runner = unittest.TextTestRunner()
    # runner.run(suite)
