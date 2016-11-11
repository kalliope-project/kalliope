import unittest


from core.OrderAnalyser import OrderAnalyser
from core.Models.Neuron import Neuron
from core.Models.Synapse import Synapse
from core.Models.Order import Order


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

    def test_associate_order_params_to_values(self):
       ##
       # Testing the brackets position behaviour
       ##

       # Success
       order_brain = "This is the {{ variable }}"
       order_user = "This is the value"
       expected_result = {'variable': 'value'}
       self.assertEqual(OrderAnalyser._associate_order_params_to_values(order_user,order_brain), expected_result,
                        "Fail to match the order_brain {{ variable }} to the 'value'")

       # Success
       order_brain = "This is the {{variable }}"
       order_user = "This is the value"
       expected_result = {'variable': 'value'}
       self.assertEqual(OrderAnalyser._associate_order_params_to_values(order_user, order_brain), expected_result,
                        "Fail to match the order_brain {{variable }} to the 'value'")

       # Success
       order_brain = "This is the {{ variable}}"
       order_user = "This is the value"
       expected_result = {'variable': 'value'}
       self.assertEqual(OrderAnalyser._associate_order_params_to_values(order_user, order_brain), expected_result,
                        "Fail to match the order_brain {{ variable}} to the 'value'")

       # Success
       order_brain = "This is the {{variable}}"
       order_user = "This is the value"
       expected_result = {'variable': 'value'}
       self.assertEqual(OrderAnalyser._associate_order_params_to_values(order_user, order_brain), expected_result,
                        "Fail to match the order_brain {{variable}} to the 'value'")

       # Fail
       order_brain = "This is the {variable}"
       order_user = "This is the value"
       expected_result = {'variable': 'value'}
       self.assertNotEquals(OrderAnalyser._associate_order_params_to_values(order_user, order_brain), expected_result,
                        "Should not match the order_brain {variable} to the 'value'")

       # Fail
       order_brain = "This is the { variable}}"
       order_user = "This is the value"
       expected_result = {'variable': 'value'}
       self.assertNotEquals(OrderAnalyser._associate_order_params_to_values(order_user, order_brain), expected_result,
                        "Should not match the order_brain { variable}} to the 'value'")

       ##
       # Testing the brackets position in the sentence
       ##

       # Success
       order_brain = "{{ variable }} This is the"
       order_user = "value This is the"
       expected_result = {'variable': 'value'}
       self.assertEqual(OrderAnalyser._associate_order_params_to_values(order_user, order_brain), expected_result,
                         "Fail to match the order_brain {{ variable }} in first position ins the sentence to the 'value'")

       # Success
       order_brain = "This is {{ variable }} the"
       order_user = " This is value the"
       expected_result = {'variable': 'value'}
       self.assertEqual(OrderAnalyser._associate_order_params_to_values(order_user, order_brain), expected_result,
                         "Fail to match the order_brain {{ variable }} in middle position ins the sentence to the 'value'")


       ##
       # Testing multi variables
       ##

       # Success
       order_brain = "This is {{ variable }} the {{ variable2 }}"
       order_user = "This is value the value2"
       expected_result = {'variable': 'value',
                          'variable2': 'value2'}
       self.assertEqual(OrderAnalyser._associate_order_params_to_values(order_user, order_brain), expected_result,
                        "Fail to match the order_brain multi variable to the multi values")

       ##
       # Testing multi words in variable
       ##

       # Success
       order_brain = "This is the {{ variable }}"
       order_user = "This is the value with multiple words"
       expected_result = {'variable': 'value with multiple words'}
       self.assertEqual(OrderAnalyser._associate_order_params_to_values(order_user,order_brain), expected_result,
                        "Fail to match the order_brain {{ variable }} to the 'value with multiple words'")

       # Success
       order_brain = "This is the {{ variable }} and  {{ variable2 }}"
       order_user = "This is the value with multiple words and second value multiple"
       expected_result = {'variable': 'value with multiple words',
                          'variable2': 'second value multiple'}
       self.assertEqual(OrderAnalyser._associate_order_params_to_values(order_user,order_brain), expected_result,
                        "Fail to match the order_brain multiple variables with multiple words as values'")


    def test_get_matching_synapse_list(self):
        # Init
        neuron1 = Neuron(name='neurone1', parameters={'var1':'val1'})
        neuron2 = Neuron(name='neurone2', parameters={'var2': 'val2'})
        neuron3 = Neuron(name='neurone3', parameters={'var3': 'val3'})
        neuron4 = Neuron(name='neurone4', parameters={'var4': 'val4'})

        signal1 = Order(sentence="this is the sentence")
        signal2 = Order(sentence="this is the second sentence")
        signal3 = Order(sentence="this is the third sentence")

        synapse1 = Synapse(name="Synapse1",neurons={neuron1, neuron2}, signals={signal1})
        synapse2 = Synapse(name="Synapse2", neurons={neuron3, neuron4}, signals={signal2})
        synapse3 = Synapse(name="Synapse3", neurons={neuron2, neuron4}, signals={signal3})

        order_to_match = "this is the sentence"
        all_synapse_list = [synapse1,
                            synapse2,
                            synapse3]

        expected_result = [synapse1]

        # Success
        self.assertEquals(OrderAnalyser._get_matching_synapse_list(all_synapses_list=all_synapse_list, order_to_match=order_to_match),
                          expected_result,
                          "Fail matching the expected synapse from the complete synapse list and the order")

        # TODO : to be continued

    def test_get_synapse_params(self):
        # Init
        neuron1 = Neuron(name='neurone1', parameters={'var1': 'val1'})
        neuron2 = Neuron(name='neurone2', parameters={'var2': 'val2'})

        signal1 = Order(sentence="this is the {{ sentence }}")

        synapse1 = Synapse(name="Synapse1", neurons={neuron1, neuron2}, signals={signal1})

        order_to_check = "this is the value"
        expected_resut = {'sentence':'value'}

        self.assertEquals(OrderAnalyser._get_synapse_params(synapse=synapse1, order_to_check=order_to_check),
                          expected_resut,
                          "Fail to retrieve the params of the synapse from the order")

        # TODO : to be continued


if __name__ == '__main__':
    unittest.main()