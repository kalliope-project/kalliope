import unittest

from kalliope.core.NeuronParameterLoader import NeuronParameterLoader


class TestNeuronParameterLoader(unittest.TestCase):

    def test_get_parameters(self):

        synapse_order = "this is the {{ sentence }}"
        user_order = "this is the value"
        expected_result = {'sentence': 'value'}

        self.assertEqual(NeuronParameterLoader.get_parameters(synapse_order=synapse_order, user_order=user_order),
                         expected_result,
                         "Fail to retrieve 'the params' of the synapse_order from the order")

        # Multiple match
        synapse_order = "this is the {{ sentence }}"

        user_order = "this is the value with multiple words"
        expected_result = {'sentence': 'value with multiple words'}

        self.assertEqual(NeuronParameterLoader.get_parameters(synapse_order=synapse_order, user_order=user_order),
                         expected_result,
                         "Fail to retrieve the 'multiple words params' of the synapse_order from the order")

        # Multiple params
        synapse_order = "this is the {{ sentence }} with multiple {{ params }}"

        user_order = "this is the value with multiple words"
        expected_result = {'sentence': 'value',
                           'params':'words'}

        self.assertEqual(NeuronParameterLoader.get_parameters(synapse_order=synapse_order, user_order=user_order),
                         expected_result,
                         "Fail to retrieve the 'multiple params' of the synapse_order from the order")

        # Multiple params with multiple words
        synapse_order = "this is the {{ sentence }} with multiple {{ params }}"

        user_order = "this is the multiple values with multiple values as words"
        expected_result = {'sentence': 'multiple values',
                           'params': 'values as words'}

        self.assertEqual(NeuronParameterLoader.get_parameters(synapse_order=synapse_order, user_order=user_order),
                         expected_result)

        # params at the begining of the sentence
        synapse_order = "{{ sentence }} this is the sentence"

        user_order = "hello world this is the multiple values with multiple values as words"
        expected_result = {'sentence': 'hello world'}

        self.assertEqual(NeuronParameterLoader.get_parameters(synapse_order=synapse_order, user_order=user_order),
                         expected_result)

        # all of the sentence is a variable
        synapse_order = "{{ sentence }}"

        user_order = "this is the all sentence is a variable"
        expected_result = {'sentence': 'this is the all sentence is a variable'}

        self.assertEqual(NeuronParameterLoader.get_parameters(synapse_order=synapse_order, user_order=user_order),
                         expected_result)

    def test_associate_order_params_to_values(self):
        ##
        # Testing the brackets position behaviour
        ##

        # Success
        order_brain = "This is the {{ variable }}"
        order_user = "This is the value"
        expected_result = {'variable': 'value'}
        self.assertEqual(NeuronParameterLoader._associate_order_params_to_values(order_user, order_brain),
                         expected_result)

        # Success
        order_brain = "This is the {{variable }}"
        order_user = "This is the value"
        expected_result = {'variable': 'value'}
        self.assertEqual(NeuronParameterLoader._associate_order_params_to_values(order_user, order_brain),
                         expected_result)

        # Success
        order_brain = "This is the {{ variable}}"
        order_user = "This is the value"
        expected_result = {'variable': 'value'}
        self.assertEqual(NeuronParameterLoader._associate_order_params_to_values(order_user, order_brain),
                         expected_result)

        # Success
        order_brain = "This is the {{variable}}"
        order_user = "This is the value"
        expected_result = {'variable': 'value'}
        self.assertEqual(NeuronParameterLoader._associate_order_params_to_values(order_user, order_brain),
                         expected_result)

        # Fail
        order_brain = "This is the {variable}"
        order_user = "This is the value"
        expected_result = {'variable': 'value'}
        self.assertNotEqual(NeuronParameterLoader._associate_order_params_to_values(order_user, order_brain),
                             expected_result)

        # Fail
        order_brain = "This is the { variable}}"
        order_user = "This is the value"
        expected_result = {'variable': 'value'}
        self.assertNotEqual(NeuronParameterLoader._associate_order_params_to_values(order_user, order_brain),
                             expected_result)

        ##
        # Testing the brackets position in the sentence
        ##

        # Success
        order_brain = "{{ variable }} This is the"
        order_user = "value This is the"
        expected_result = {'variable': 'value'}
        self.assertEqual(NeuronParameterLoader._associate_order_params_to_values(order_user, order_brain),
                         expected_result)

        # Success
        order_brain = "This is {{ variable }} the"
        order_user = " This is value the"
        expected_result = {'variable': 'value'}
        self.assertEqual(NeuronParameterLoader._associate_order_params_to_values(order_user, order_brain),
                         expected_result)

        ##
        # Testing multi variables
        ##

        # Success
        order_brain = "This is {{ variable }} the {{ variable2 }}"
        order_user = "This is value the value2"
        expected_result = {'variable': 'value',
                           'variable2': 'value2'}
        self.assertEqual(NeuronParameterLoader._associate_order_params_to_values(order_user, order_brain),
                         expected_result)

        ##
        # Testing multi words in variable
        ##

        # Success
        order_brain = "This is the {{ variable }}"
        order_user = "This is the value with multiple words"
        expected_result = {'variable': 'value with multiple words'}
        self.assertEqual(NeuronParameterLoader._associate_order_params_to_values(order_user, order_brain),
                         expected_result)

        # Success
        order_brain = "This is the {{ variable }} and  {{ variable2 }}"
        order_user = "This is the value with multiple words and second value multiple"
        expected_result = {'variable': 'value with multiple words',
                           'variable2': 'second value multiple'}
        self.assertEqual(NeuronParameterLoader._associate_order_params_to_values(order_user, order_brain),
                         expected_result)

        ##
        #  Specific Behaviour
        ##

        # Upper/Lower case
        order_brain = "This Is The {{ variable }}"
        order_user = "ThiS is tHe VAlue"
        expected_result = {'variable': 'VAlue'}
        self.assertEqual(NeuronParameterLoader._associate_order_params_to_values(order_user, order_brain),
                         expected_result)

if __name__ == '__main__':
    unittest.main()