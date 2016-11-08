import unittest

from core.OrderAnalyser import OrderAnalyser


class TestOrderAnalyser(unittest.TestCase):

    """Test case for the OrderAnalyser Class"""

    def test_is_containing_bracket(self):
        #  Success
        order_to_test = "This test contains {{ bracket }}"
        self.assertTrue(OrderAnalyser._is_containing_bracket(order_to_test),
                        "Fail returning True when order contains spaced brackets")

        order_to_test = "This test contains {{bracket }}"
        self.assertTrue(OrderAnalyser._is_containing_bracket(order_to_test),
                        "Fail returning True when order contains right spaced bracket")

        order_to_test = "This test contains {{ bracket}}"
        self.assertTrue(OrderAnalyser._is_containing_bracket(order_to_test),
                        "Fail returning True when order contains left spaced bracket")

        order_to_test = "This test contains {{bracket}}"
        self.assertTrue(OrderAnalyser._is_containing_bracket(order_to_test),
                        "Fail returning True when order contains no spaced bracket")

        #  Failure
        order_to_test = "This test does not contain bracket"
        self.assertFalse(OrderAnalyser._is_containing_bracket(order_to_test),
                        "Fail returning False when order has no brackets")

        #  Behaviour
        order_to_test = ""
        self.assertFalse(OrderAnalyser._is_containing_bracket(order_to_test),
                        "Fail returning False when no order")

    def test_get_next_value_list(self):
        # Success
        list_to_test = {1, 2, 3}
        self.assertEqual(OrderAnalyser._get_next_value_list(list_to_test),2,
                         "Fail to match the expected next value from the list")

        # Failure
        list_to_test = {1}
        self.assertEqual(OrderAnalyser._get_next_value_list(list_to_test), None,
                         "Fail to ensure there is no next value from the list")

        # Behaviour
        list_to_test = {}
        self.assertEqual(OrderAnalyser._get_next_value_list(list_to_test), None,
                         "Fail to ensure the empty list return None value")

    def test_spelt_order_match_brain_order_via_table(self):
        order_to_test = "this is the order"
        sentence_to_test = "this is the order"

        # Success
        self.assertTrue(OrderAnalyser._spelt_order_match_brain_order_via_table(order_to_test, sentence_to_test),
                        "Fail matching order with the expected sentence")

        # Failure
        sentence_to_test = "unexpected sentence"
        self.assertFalse(OrderAnalyser._spelt_order_match_brain_order_via_table(order_to_test, sentence_to_test),
                         "Fail to ensure the expected sentence is not matching the order")

    def test_get_split_order_without_bracket(self):

        # Success
        order_to_test = "this is the order"
        expected_result = ["this", "is", "the", "order"]
        self.assertEqual(OrderAnalyser._get_split_order_without_bracket(order_to_test),expected_result,
                         "No brackets Fails to return the expected list")

        order_to_test = "this is the {{ order }}"
        expected_result = ["this", "is", "the"]
        self.assertEqual(OrderAnalyser._get_split_order_without_bracket(order_to_test), expected_result,
                         "With spaced brackets Fails to return the expected list")

        order_to_test = "this is the {{order }}" # left bracket without space
        expected_result = ["this", "is", "the"]
        self.assertEqual(OrderAnalyser._get_split_order_without_bracket(order_to_test), expected_result,
                         "Left brackets Fails to return the expected list")

        order_to_test = "this is the {{ order}}" # right bracket without space
        expected_result = ["this", "is", "the"]
        self.assertEqual(OrderAnalyser._get_split_order_without_bracket(order_to_test), expected_result,
                         "Right brackets Fails to return the expected list")

        order_to_test = "this is the {{order}}"  # bracket without space
        expected_result = ["this", "is", "the"]
        self.assertEqual(OrderAnalyser._get_split_order_without_bracket(order_to_test), expected_result,
                         "No space brackets Fails to return the expected list")

if __name__ == '__main__':
    unittest.main()