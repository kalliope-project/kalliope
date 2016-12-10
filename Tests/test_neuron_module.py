import os
import unittest
import mock

from kalliope.core.NeuronModule import NeuronModule, TemplateFileNotFoundException


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
