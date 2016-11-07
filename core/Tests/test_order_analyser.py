import unittest

from core.OrderAnalyser import OrderAnalyser


class TestOrderAnalyser(unittest.TestCase):

    """Test case for the OrderAnalyser Class"""

    def test_is_containing_bracket(self):
        #  Success
        self.assertTrue(OrderAnalyser._is_containing_bracket("This test contains {{ bracket }}"))

        #  Failure
        self.assertFalse(OrderAnalyser._is_containing_bracket("This test does not contain bracket"))

    def test_get_next_value_list(self):
        # Success
        list_to_test = {1, 2, 3}
        self.assertEqual(OrderAnalyser._get_next_value_list(list_to_test),2)

        # Failure
        list_to_test = {1}
        self.assertEqual(OrderAnalyser._get_next_value_list(list_to_test), None)

        # Behaviour
        list_to_test = {}
        self.assertEqual(OrderAnalyser._get_next_value_list(list_to_test), None)

    def test_spelt_order_match_brain_order_via_table(self):
        order_to_test = "this is the order"
        sentence_to_test = "this is the order"

        # Success
        self.assertTrue(OrderAnalyser._spelt_order_match_brain_order_via_table(order_to_test,
                                                                               sentence_to_test))

        # Failure
        sentence_to_test = "unexpected sentence"
        self.assertFalse(OrderAnalyser._spelt_order_match_brain_order_via_table(order_to_test,
                                                                                 sentence_to_test))

if __name__ == '__main__':
    unittest.main()