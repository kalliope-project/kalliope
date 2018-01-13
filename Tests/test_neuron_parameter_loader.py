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
                           'params': 'words'}

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

        # Upper/Lower case between multiple variables
        order_brain = "This Is The {{ variable }} And The {{ variable2 }}"
        order_user = "ThiS is tHe VAlue aND tHE vAlUe2"
        expected_result = {'variable': 'VAlue',
                           'variable2': 'vAlUe2'}
        self.assertEqual(NeuronParameterLoader._associate_order_params_to_values(order_user, order_brain),
                         expected_result)

        # Upper/Lower case between multiple variables and at the End
        order_brain = "This Is The {{ variable }} And The {{ variable2 }} And Again"
        order_user = "ThiS is tHe VAlue aND tHE vAlUe2 and aGAIN"
        expected_result = {'variable': 'VAlue',
                           'variable2': 'vAlUe2'}
        self.assertEqual(NeuronParameterLoader._associate_order_params_to_values(order_user, order_brain),
                         expected_result)

        # integers variables
        order_brain = "This Is The {{ variable }} And The {{ variable2 }}"
        order_user = "ThiS is tHe 1 aND tHE 2"
        expected_result = {'variable': '1',
                           'variable2': '2'}
        self.assertEqual(NeuronParameterLoader._associate_order_params_to_values(order_user, order_brain),
                         expected_result)

        # ##
        # #  More words in the order brain.
        # #  /!\ Not working but not needed !
        # ##
        #
        # # more words in the middle of order but matching
        # order_brain = "this is the {{ variable }} and the {{ variable2 }}"
        # order_user = "this the foo and the bar" # missing "is" but matching because all words are present !
        # expected_result = {'variable': 'foo',
        #                    'variable2': 'bar'}
        # self.assertEqual(NeuronParameterLoader._associate_order_params_to_values(order_user, order_brain),
        #                  expected_result)
        #
        # # more words in the beginning of order but matching +  bonus with mixed uppercases
        # order_brain = "blaBlabla bla This Is The {{ variable }} And The {{ variable2 }}"
        # order_user = "ThiS is tHe foo aND tHE bar"
        # expected_result = {'variable': 'foo',
        #                    'variable2': 'bar'}
        # self.assertEqual(NeuronParameterLoader._associate_order_params_to_values(order_user, order_brain),
        #                  expected_result)
        #
        # # more words in the end of order but matching +  bonus with mixed uppercases
        # order_brain = "This Is The bla BLa bla BLa {{ variable }} And The {{ variable2 }}"
        # order_user = "ThiS is tHe foo aND tHE bar"
        # expected_result = {'variable': 'foo',
        #                    'variable2': 'bar'}
        # self.assertEqual(NeuronParameterLoader._associate_order_params_to_values(order_user, order_brain),
        #                  expected_result)
        #
        # # complex more words in the end of order but matching +  bonus with mixed uppercases
        # order_brain = "Hi theRe This Is bla BLa The bla BLa {{ variable }} And The {{ variable2 }}"
        # order_user = "ThiS is tHe foo aND tHE bar"
        # expected_result = {'variable': 'foo',
        #                    'variable2': 'bar'}
        # self.assertEqual(NeuronParameterLoader._associate_order_params_to_values(order_user, order_brain),
        #                  expected_result)
        #
        # # complex more words everywhere in the order but matching +  bonus with mixed uppercases
        # order_brain = "Hi theRe This Is bla BLa The bla BLa {{ variable }} And Oops The {{ variable2 }} Oopssss"
        # order_user = "ThiS is tHe foo aND tHE bar"
        # expected_result = {'variable': 'foo',
        #                    'variable2': 'bar'}
        # self.assertEqual(NeuronParameterLoader._associate_order_params_to_values(order_user, order_brain),
        #                  expected_result)
        #

        ##
        #  More words in the user order brain
        ##

        # 1 not matching word in the middle of user order but matching
        order_brain = "this the {{ variable }} and the {{ variable2 }}"
        order_user = "this is the foo and the bar"  # adding "is" but matching because all words are present !
        expected_result = {'variable': 'foo',
                           'variable2': 'bar'}
        self.assertEqual(NeuronParameterLoader._associate_order_params_to_values(order_user, order_brain),
                         expected_result)

        # 2 not matching  words in the middle of user order but matching
        order_brain = "this the {{ variable }} and the {{ variable2 }}"
        order_user = "this is Fake the foo and the bar"
        expected_result = {'variable': 'foo',
                           'variable2': 'bar'}
        self.assertEqual(NeuronParameterLoader._associate_order_params_to_values(order_user, order_brain),
                         expected_result)

        # 1 not matching word at the beginning and 1 not matching word in the middle of user order but matching
        order_brain = "this the {{ variable }} and the {{ variable2 }}"
        order_user = "Oops this is the foo and the bar"
        expected_result = {'variable': 'foo',
                           'variable2': 'bar'}
        self.assertEqual(NeuronParameterLoader._associate_order_params_to_values(order_user, order_brain),
                         expected_result)

        # 2 not matching words at the beginning and 2 not matching words in the middle of user order but matching
        order_brain = "this the {{ variable }} and the {{ variable2 }}"
        order_user = "Oops Oops this is BlaBla the foo and the bar"
        expected_result = {'variable': 'foo',
                           'variable2': 'bar'}
        self.assertEqual(NeuronParameterLoader._associate_order_params_to_values(order_user, order_brain),
                         expected_result)

        # Adding complex not matching words in the middle of user order and between variable but matching
        order_brain = "this the {{ variable }} and the {{ variable2 }}"
        order_user = "Oops Oops this is BlaBla the foo and ploup ploup the bar"
        expected_result = {'variable': 'foo',
                           'variable2': 'bar'}
        self.assertEqual(NeuronParameterLoader._associate_order_params_to_values(order_user, order_brain),
                         expected_result)

        # Adding complex not matching words in the middle of user order and between variable and at the end but matching
        order_brain = "this the {{ variable }} and the {{ variable2 }} hello"
        order_user = "Oops Oops this is BlaBla the foo and ploup ploup the bar hello test"
        expected_result = {'variable': 'foo',
                           'variable2': 'bar'}
        self.assertEqual(NeuronParameterLoader._associate_order_params_to_values(order_user, order_brain),
                         expected_result)


if __name__ == '__main__':
    unittest.main()
