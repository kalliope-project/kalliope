import os
import unittest
import mock

from kalliope.core.NeuronModule import NeuronModule, TemplateFileNotFoundException
from kalliope.core.Models.Neuron import Neuron
from kalliope.core.Models.Synapse import Synapse
from kalliope.core.Models.Brain import Brain
from kalliope.core.Models.Order import Order


class TestNeuronModule(unittest.TestCase):

    def setUp(self):
        self.expected_result = "hello, this is a replaced word"
        # this allow us to run the test from an IDE and from the root with python -m unittest Tests.TestNeuronModule
        if "/Tests" in os.getcwd():
            self.file_template = "templates/template_test.j2"
        else:
            self.file_template = "Tests/templates/template_test.j2"
        self.say_template = "hello, this is a {{ test }}"
        self.message = {
            "test": "replaced word"
        }
        self.neuron_module_test = NeuronModule()

    def tearDown(self):
        del self.neuron_module_test

    def test_get_audio_from_stt(self):
        """
        Test the OrderListener thread is started
        """

        with mock.patch("kalliope.core.OrderListener.start") as mock_orderListener_start:
            with mock.patch("kalliope.core.OrderListener.join") as mock_orderListener_join:
                def callback():
                    pass
                NeuronModule.get_audio_from_stt(callback=callback())
                mock_orderListener_start.assert_called_once_with()
                mock_orderListener_start.reset_mock()

    def test_update_cache_var(self):
        """
        Test Update the value of the cache in the provided arg list
        """

        # True -> False
        args_dict = {
            "cache": True
        }
        expected_dict = {
            "cache": False
        }
        self.assertEquals(NeuronModule._update_cache_var(False, args_dict=args_dict),
                          expected_dict,
                          "Fail to update the cache value from True to False")
        self.assertFalse(args_dict["cache"])

        # False -> True
        args_dict = {
            "cache": False
        }
        expected_dict = {
            "cache": True
        }
        self.assertEquals(NeuronModule._update_cache_var(True, args_dict=args_dict),
                          expected_dict,
                          "Fail to update the cache value from False to True")

        self.assertTrue(args_dict["cache"])

    def test_get_message_from_dict(self):

        self.neuron_module_test.say_template = self.say_template

        self.assertEqual(self.neuron_module_test._get_message_from_dict(self.message), self.expected_result)
        del self.neuron_module_test
        self.neuron_module_test = NeuronModule()

        # test with file_template
        self.neuron_module_test.file_template = self.file_template
        self.assertEqual(self.neuron_module_test._get_message_from_dict(self.message), self.expected_result)
        del self.neuron_module_test

        # test with no say_template and no file_template
        self.neuron_module_test = NeuronModule()
        self.assertEqual(self.neuron_module_test._get_message_from_dict(self.message), None)

    def test_get_say_template(self):
        # test with a string
        self.assertEqual(NeuronModule._get_say_template(self.say_template, self.message), self.expected_result)

        # test with a list
        say_template = list()
        say_template.append("hello, this is a {{ test }} one")
        say_template.append("hello, this is a {{ test }} two")
        expected_result = list()
        expected_result.append("hello, this is a replaced word one")
        expected_result.append("hello, this is a replaced word two")
        self.assertTrue(NeuronModule._get_say_template(say_template, self.message) in expected_result)

    def test_get_file_template(self):
        # test with a valid template
        self.assertEqual(NeuronModule._get_file_template(self.file_template, self.message), self.expected_result)

        # test raise with a non existing template
        file_template = "does_not_exist.j2"
        with self.assertRaises(TemplateFileNotFoundException):
            NeuronModule._get_file_template(file_template, self.message)

    def test_get_content_of_file(self):
        expected_result = "hello, this is a {{ test }}"
        self.assertEqual(NeuronModule._get_content_of_file(self.file_template), expected_result)

    def test_run_synapse_by_name_with_order(self):
        """
        Test to start a synapse with a specific given order
        Scenarii :
            - Neuron has been found and launched
            - Neuron has not been found
        """

        # Init
        neuron1 = Neuron(name='neurone1', parameters={'var1': 'val1'})
        neuron2 = Neuron(name='neurone2', parameters={'var2': 'val2'})
        neuron3 = Neuron(name='neurone3', parameters={'var3': 'val3'})
        neuron4 = Neuron(name='neurone4', parameters={'var4': 'val4'})

        signal1 = Order(sentence="the sentence")
        signal2 = Order(sentence="the second sentence")
        signal3 = Order(sentence="part of the third sentence")

        synapse1 = Synapse(name="Synapse1", neurons=[neuron1, neuron2], signals=[signal1])
        synapse2 = Synapse(name="Synapse2", neurons=[neuron3, neuron4], signals=[signal2])
        synapse3 = Synapse(name="Synapse3", neurons=[neuron2, neuron4], signals=[signal3])

        all_synapse_list = [synapse1,
                            synapse2,
                            synapse3]

        br = Brain(synapses=all_synapse_list)

        order = "This is the order"
        synapse_name = "Synapse2"
        answer = "This is the {{ answer }}"

        with mock.patch("kalliope.core.OrderAnalyser.start") as mock_orderAnalyser_start:
            neuron_mod = NeuronModule()
            neuron_mod.brain = br

            # Success
            self.assertTrue(neuron_mod.run_synapse_by_name_with_order(order=order,
                                                                        synapse_name=synapse_name,
                                                                        order_template=answer),
                              "fail to find the proper synapse")

            # mock_orderAnalyser_start.assert_called_once()
            mock_orderAnalyser_start.assert_called_once_with(synapses_to_run=[synapse2],
                                                             external_order=answer)
            mock_orderAnalyser_start.reset_mock()

            # Fail
            synapse_name = "Synapse5"
            self.assertFalse(neuron_mod.run_synapse_by_name_with_order(order=order,
                                                                      synapse_name=synapse_name,
                                                                       order_template=answer),
                            "fail to NOT find the synapse")

            mock_orderAnalyser_start.assert_not_called()
            mock_orderAnalyser_start.reset_mock()



