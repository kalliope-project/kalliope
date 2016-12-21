import unittest
import mock

from kalliope.core.OrderAnalyser import OrderAnalyser
from kalliope.core.Models.Neuron import Neuron
from kalliope.core.Models.Synapse import Synapse
from kalliope.core.Models.Brain import Brain
from kalliope.core.Models.Settings import Settings
from kalliope.core.Models.Order import Order


class TestOrderAnalyser(unittest.TestCase):

    """Test case for the OrderAnalyser Class"""

    def setUp(self):
        pass

    def test_start(self):
        """
        Testing if the matches from the incoming messages and the signals/order sentences.
        Scenarii :
            - Order matchs a synapse and the synapse has been launched.
            - Order does not match but have a default synapse.
            - Order does not match and does not have default synapse.
            - Provide synapse without any external orders
            - Provide synapse with any external orders
        """
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

        with mock.patch("kalliope.core.OrderAnalyser._start_neuron") as mock_start_neuron_method:
            # assert synapses have been launched
            order_to_match = "this is the sentence"
            oa = OrderAnalyser(order=order_to_match,
                               brain=br)
            expected_result = [synapse1]

            self.assertEquals(oa.start(),
                              expected_result,
                              "Fail to run the expected Synapse matching the order")

            calls = [mock.call(neuron1, {}), mock.call(neuron2, {})]
            mock_start_neuron_method.assert_has_calls(calls=calls)
            mock_start_neuron_method.reset_mock()

            # No order matching Default Synapse to run
            order_to_match = "random sentence"
            oa = OrderAnalyser(order=order_to_match,
                               brain=br)
            oa.settings = mock.MagicMock(default_synapse="Synapse3")
            expected_result = [synapse3]
            self.assertEquals(oa.start(),
                              expected_result,
                              "Fail to run the default Synapse because no other synapses match the order")

            # No order matching no Default Synapse
            order_to_match = "random sentence"
            oa = OrderAnalyser(order=order_to_match,
                               brain=br)
            oa.settings = mock.MagicMock()
            expected_result = []
            self.assertEquals(oa.start(),
                              expected_result,
                              "Fail to no synapse because no synapse matchs and no default defined")

            # Provide synapse to run
            order_to_match = "this is the sentence"
            oa = OrderAnalyser(order=order_to_match,
                               brain=br)
            expected_result = [synapse1]
            synapses_to_run = [synapse1]

            self.assertEquals(oa.start(synapses_to_run=synapses_to_run),
                              expected_result,
                              "Fail to run the provided synapse to run")
            calls = [mock.call(neuron1, {}), mock.call(neuron2, {})]
            mock_start_neuron_method.assert_has_calls(calls=calls)
            mock_start_neuron_method.reset_mock()

            # Provide synapse and external orders
            order_to_match = "this is an external sentence"
            oa = OrderAnalyser(order=order_to_match,
                               brain=br)
            external_orders = "this is an external {{ order }}"
            synapses_to_run = [synapse2]
            expected_result = [synapse2]

            self.assertEquals(oa.start(synapses_to_run=synapses_to_run, external_order=external_orders),
                              expected_result,
                              "Fail to run a provided synapse with external order")
            calls = [mock.call(neuron3, {"order":u"sentence"}), mock.call(neuron4, {"order":u"sentence"})]
            mock_start_neuron_method.assert_has_calls(calls=calls)
            mock_start_neuron_method.reset_mock()

    def test_start_neuron(self):
        """
        Testing params association and starting a Neuron
        """

        neuron4 = Neuron(name='neurone4', parameters={'var4': 'val4'})

        with mock.patch("kalliope.core.NeuronLauncher.NeuronLauncher.start_neuron") as mock_start_neuron_method:
            # Assert to the neuron is launched
            neuron1 = Neuron(name='neurone1', parameters={'var1': 'val1'})
            params = {
                'param1':'parval1'
            }
            OrderAnalyser._start_neuron(neuron=neuron1,params=params)
            mock_start_neuron_method.assert_called_with(neuron1)
            mock_start_neuron_method.reset_mock()

            # Assert the params are well passed to the neuron
            neuron2 = Neuron(name='neurone2', parameters={'var2': 'val2', 'args': ['arg1', 'arg2']})
            params = {
                'arg1':'argval1',
                'arg2':'argval2'
            }
            OrderAnalyser._start_neuron(neuron=neuron2, params=params)
            neuron2_params = Neuron(name='neurone2',
                                    parameters={'var2': 'val2',
                                                'args': ['arg1', 'arg2'],
                                                'arg1':'argval1',
                                                'arg2':'argval2'}
                                    )
            mock_start_neuron_method.assert_called_with(neuron2_params)
            mock_start_neuron_method.reset_mock()

            # Assert the Neuron is not started when missing args
            neuron3 = Neuron(name='neurone3', parameters={'var3': 'val3', 'args': ['arg3', 'arg4']})
            params = {
                'arg1': 'argval1',
                'arg2': 'argval2'
            }
            OrderAnalyser._start_neuron(neuron=neuron3, params=params)
            mock_start_neuron_method.assert_not_called()
            mock_start_neuron_method.reset_mock()

            # Assert no neuron is launched when waiting for args and none are given
            neuron4 = Neuron(name='neurone4', parameters={'var4': 'val4', 'args': ['arg5', 'arg6']})
            params = {}
            OrderAnalyser._start_neuron(neuron=neuron4, params=params)
            mock_start_neuron_method.assert_not_called()
            mock_start_neuron_method.reset_mock()


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
        self.assertEqual(OrderAnalyser._get_next_value_list(list_to_test), 2,
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
        self.assertTrue(OrderAnalyser.spelt_order_match_brain_order_via_table(order_to_test, sentence_to_test),
                        "Fail matching order with the expected sentence")

        # Failure
        sentence_to_test = "unexpected sentence"
        self.assertFalse(OrderAnalyser.spelt_order_match_brain_order_via_table(order_to_test, sentence_to_test),
                         "Fail to ensure the expected sentence is not matching the order")

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

    def test_associate_order_params_to_values(self):
        ##
        # Testing the brackets position behaviour
        ##

        # Success
        order_brain = "This is the {{ variable }}"
        order_user = "This is the value"
        expected_result = {'variable': 'value'}
        self.assertEqual(OrderAnalyser._associate_order_params_to_values(order_user, order_brain), expected_result,
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
                         "Fail to match the order_brain {{ variable }} in first position "
                         "ins the sentence to the 'value'")

        # Success
        order_brain = "This is {{ variable }} the"
        order_user = " This is value the"
        expected_result = {'variable': 'value'}
        self.assertEqual(OrderAnalyser._associate_order_params_to_values(order_user, order_brain), expected_result,
                         "Fail to match the order_brain {{ variable }} in middle position ins "
                         "the sentence to the 'value'")

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
        self.assertEqual(OrderAnalyser._associate_order_params_to_values(order_user, order_brain), expected_result,
                         "Fail to match the order_brain {{ variable }} to the 'value with multiple words'")

        # Success
        order_brain = "This is the {{ variable }} and  {{ variable2 }}"
        order_user = "This is the value with multiple words and second value multiple"
        expected_result = {'variable': 'value with multiple words',
                           'variable2': 'second value multiple'}
        self.assertEqual(OrderAnalyser._associate_order_params_to_values(order_user, order_brain), expected_result,
                         "Fail to match the order_brain multiple variables with multiple words as values'")

    def test_get_matching_synapse_list(self):
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

        order_to_match = "this is the sentence"
        all_synapse_list = [synapse1,
                            synapse2,
                            synapse3]



        # Success
        expected_result = synapse1
        oa_tuple_list = OrderAnalyser._get_matching_synapse_list(all_synapses_list=all_synapse_list,
                                                                   order_to_match=order_to_match)
        self.assertEquals(oa_tuple_list[0].synapse,
                          expected_result,
                          "Fail matching 'the expected synapse' from the complete synapse list and the order")

        # Multiple Matching synapses
        signal2 = Order(sentence="this is the sentence")

        synapse2 = Synapse(name="Synapse2", neurons=[neuron3, neuron4], signals=[signal2])
        order_to_match = "this is the sentence"

        all_synapse_list = [synapse1,
                            synapse2,
                            synapse3]

        expected_result = [synapse1,
                           synapse2]
        oa_tuple_list = OrderAnalyser._get_matching_synapse_list(all_synapses_list=all_synapse_list,
                                                                 order_to_match=order_to_match)
        self.assertEquals(oa_tuple_list[0].synapse,
                          expected_result[0],
                          "Fail 'Multiple Matching synapses' from the complete synapse list and the order (first element)")
        self.assertEquals(oa_tuple_list[1].synapse,
                          expected_result[1],
                          "Fail 'Multiple Matching synapses' from the complete synapse list and the order (second element)")

        # matching no synapses
        order_to_match = "this is not the correct word"

        all_synapse_list = [synapse1,
                            synapse2,
                            synapse3]

        expected_result = []

        self.assertEquals(OrderAnalyser._get_matching_synapse_list(all_synapses_list=all_synapse_list,
                                                                   order_to_match=order_to_match),
                          expected_result,
                          "Fail matching 'no synapses' from the complete synapse list and the order")

        # matching synapse with all key worlds
        # /!\ Some words in the order are matching all words in synapses signals !
        order_to_match = "this is not the correct sentence"
        all_synapse_list = [synapse1,
                            synapse2,
                            synapse3]

        expected_result = [synapse1,
                           synapse2]

        oa_tuple_list = OrderAnalyser._get_matching_synapse_list(all_synapses_list=all_synapse_list,
                                                                 order_to_match=order_to_match)

        self.assertEquals(oa_tuple_list[0].synapse,
                          expected_result[0],
                          "Fail matching 'synapse with all key worlds' from the complete synapse list and the order (first element)")
        self.assertEquals(oa_tuple_list[1].synapse,
                          expected_result[1],
                          "Fail matching 'synapse with all key worlds' from the complete synapse list and the order (second element)")

    def test_get_params_from_order(self):

        string_order = "this is the {{ sentence }}"
        order_to_check = "this is the value"
        expected_result = {'sentence': 'value'}

        self.assertEquals(OrderAnalyser._get_params_from_order(string_order=string_order, order_to_check=order_to_check),
                          expected_result,
                          "Fail to retrieve 'the params' of the string_order from the order")

        # Multiple match
        string_order = "this is the {{ sentence }}"

        order_to_check = "this is the value with multiple words"
        expected_result = {'sentence': 'value with multiple words'}

        self.assertEqual(OrderAnalyser._get_params_from_order(string_order=string_order, order_to_check=order_to_check),
                         expected_result,
                         "Fail to retrieve the 'multiple words params' of the string_order from the order")

        # Multiple params
        string_order = "this is the {{ sentence }} with multiple {{ params }}"

        order_to_check = "this is the value with multiple words"
        expected_result = {'sentence': 'value',
                            'params':'words'}

        self.assertEqual(OrderAnalyser._get_params_from_order(string_order=string_order, order_to_check=order_to_check),
                         expected_result,
                         "Fail to retrieve the 'multiple params' of the string_order from the order")

        # Multiple params with multiple words
        string_order = "this is the {{ sentence }} with multiple {{ params }}"

        order_to_check = "this is the multiple values with multiple values as words"
        expected_result = {'sentence': 'multiple values',
                           'params': 'values as words'}

        self.assertEqual(OrderAnalyser._get_params_from_order(string_order=string_order, order_to_check=order_to_check),
                         expected_result,
                         "Fail to retrieve the 'multiple params with multiple words' of the string_order from the order")

        # params at the begining of the sentence
        string_order = "{{ sentence }} this is the sentence"

        order_to_check = "hello world this is the multiple values with multiple values as words"
        expected_result = {'sentence': 'hello world'}

        self.assertEqual(OrderAnalyser._get_params_from_order(string_order=string_order, order_to_check=order_to_check),
                         expected_result,
                         "Fail to retrieve the 'params at the begining of the sentence' of the string_order from the order")

        # all of the sentence is a variable
        string_order = "{{ sentence }}"

        order_to_check = "this is the all sentence is a variable"
        expected_result = {'sentence': 'this is the all sentence is a variable'}

        self.assertEqual(OrderAnalyser._get_params_from_order(string_order=string_order, order_to_check=order_to_check),
                         expected_result,
                         "Fail to retrieve the 'all of the sentence is a variable' of the string_order from the order")

    def test_get_default_synapse_from_sysnapses_list(self):
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

        default_synapse_name = "Synapse2"
        all_synapse_list = [synapse1,
                            synapse2,
                            synapse3]
        expected_result = synapse2

        # Assert equals
        self.assertEquals(OrderAnalyser._get_default_synapse_from_sysnapses_list(all_synapses_list=all_synapse_list,
                                                                                 default_synapse_name=default_synapse_name),
                          expected_result,
                          "Fail to match the expected default Synapse")

    def test_find_synapse_to_run(self):
        """
        Test to find the good synapse to run
        Scenarii:
            - Find the synapse
            - No synpase found, no default synapse
            - No synapse found, run the default synapse
        """
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
        st = Settings()
        # Find synapse
        order = "this is the sentence"
        expected_result = synapse1
        oa_tuple_list = OrderAnalyser._find_synapse_to_run(brain=br,settings=st, order=order)
        self.assertEquals(oa_tuple_list[0].synapse,
                          expected_result,
                          "Fail to run the proper synapse matching the order")

        expected_result = signal1.sentence
        self.assertEquals(oa_tuple_list[0].order,
                        expected_result,
                        "Fail to run the proper synapse matching the order")
        # No Default synapse
        order = "No default synapse"
        expected_result = []
        self.assertEquals(OrderAnalyser._find_synapse_to_run(brain=br,settings=st, order=order),
                          expected_result,
                          "Fail to run no synapse, when no default is defined")

        # Default synapse
        st = Settings(default_synapse="Synapse2")
        order = "default synapse"
        expected_result = synapse2
        oa_tuple_list = OrderAnalyser._find_synapse_to_run(brain=br, settings=st, order=order)
        self.assertEquals(oa_tuple_list[0].synapse,
                          expected_result,
                          "Fail to run the default synapse")


if __name__ == '__main__':
    unittest.main()
