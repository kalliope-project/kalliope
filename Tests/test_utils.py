#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os

import sys

from kalliope.core.Models.Neuron import Neuron
from kalliope.neurons.say.say import Say
from kalliope.core.Utils.Utils import Utils

from kalliope.core.ConfigurationManager import SettingLoader


class TestUtils(unittest.TestCase):
    """
    Class to test Utils methods
    """

    def setUp(self):
        pass

    def test_get_current_file_parent_path(self):
        """
        Expect to get back the parent path file
        """
        path_to_test = "../kalliope/core/Utils"
        expected_result = os.path.normpath("../kalliope/core")

        self.assertEqual(Utils.get_current_file_parent_path(path_to_test),
                         expected_result,
                         "fail getting the parent parent path from the given path")

    def test_get_current_file_parent_parent_path(self):
        """
        Expect to get back the parent parent path file
        """
        path_to_test = "../kalliope/core/Utils"
        expected_result = os.path.normpath("../kalliope")

        self.assertEqual(Utils.get_current_file_parent_parent_path(path_to_test),
                         expected_result,
                         "fail getting the parent parent path from the given path")

    def test_get_real_file_path(self):
        """
        Expect to load the proper file following the order :
            - Provided absolute path
            - Current user path + file_name
            - /etc/kalliope + file_name
            - /path/to/kalliope/ +file_name
        """
        ###
        # Test the absolute path
        dir_path = "/tmp/kalliope/tests/"
        file_name = "test_real_file_path"
        absolute_path_to_test = os.path.join(dir_path, file_name)
        expected_result = absolute_path_to_test
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        # touch the file
        open(absolute_path_to_test, 'a').close()

        self.assertEqual(Utils.get_real_file_path(absolute_path_to_test),
                         expected_result,
                         "Fail to match the given absolute path ")
        # Clean up
        if os.path.exists(absolute_path_to_test):
            os.remove(absolute_path_to_test)

        ###
        # test the Current path
        file_name = "test_real_file_path"
        expected_result = os.getcwd() + os.sep + file_name

        # touch the file
        open(file_name, 'a').close()

        self.assertEqual(Utils.get_real_file_path(file_name),
                         expected_result,
                         "Fail to match the Current path ")
        # Clean up
        if os.path.exists(file_name):
            os.remove(file_name)

        ###
        # test /etc/kalliope
        # /!\ need permissions
        # dir_path = "/etc/kalliope/"
        # file_name = "test_real_file_path"
        # path_to_test = os.path.join(dir_path,file_name)
        # expected_result = "/etc/kalliope" + os.sep + file_name
        # if not os.path.exists(dir_path):
        #     os.makedirs(dir_path)
        #
        # # touch the file
        # open(path_to_test, 'a').close()
        #
        # self.assertEquals(Utils.get_real_file_path(file_name),
        #                   expected_result,
        #                   "Fail to match the /etc/kalliope path")
        # # Clean up
        # if os.path.exists(file_name):
        #     os.remove(file_name)

        ###
        # /an/unknown/path/kalliope/
        dir_path = "../kalliope/"
        file_name = "test_real_file_path"
        path_to_test = os.path.join(dir_path, file_name)
        expected_result = os.path.normpath(os.getcwd() + os.sep + os.pardir + os.sep + "kalliope" + os.sep + file_name)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        # touch the file
        open(path_to_test, 'a').close()

        self.assertEqual(Utils.get_real_file_path(file_name),
                         expected_result,
                         "Fail to match the /an/unknown/path/kalliope path")
        # Clean up
        if os.path.exists(expected_result):
            os.remove(expected_result)

    def test_get_dynamic_class_instantiation(self):
        """
        Test that an instance as been instantiate properly.
        """
        sl = SettingLoader()
        sl.settings.resource_dir = '/var/tmp/test/resources'

        neuron = Neuron(name='Say', parameters={'message': 'test dynamic class instantiate'})
        say1 = Utils.get_dynamic_class_instantiation(package_name="neurons",
                                                     module_name=neuron.name.capitalize(),
                                                     parameters=neuron.parameters,
                                                     resources_dir='/var/tmp/test/resources')
        self.assertTrue(isinstance(say1, Say), "Failed to dynamically instantiate neuron 'Say'")
        say2 = Utils.get_dynamic_class_instantiation(package_name="neurons",
                                                     module_name=neuron.name.capitalize(),
                                                     parameters=neuron.parameters,
                                                     resources_dir='/var/tmp/test/resources')
        self.assertTrue(isinstance(say2, Say), "Failed to dynamically instantiate neuron 'Say'")
        self.assertNotEqual(id(say1), id(say2),
                            "Dynamic class instantiations must return unique instances")

    def test_is_containing_bracket(self):
        #  Success
        order_to_test = "This test contains {{ bracket }}"
        self.assertTrue(Utils.is_containing_bracket(order_to_test),
                        "Fail returning True when order contains spaced brackets")

        order_to_test = "This test contains {{bracket }}"
        self.assertTrue(Utils.is_containing_bracket(order_to_test),
                        "Fail returning True when order contains right spaced bracket")

        order_to_test = "This test contains {{ bracket}}"
        self.assertTrue(Utils.is_containing_bracket(order_to_test),
                        "Fail returning True when order contains left spaced bracket")

        order_to_test = "This test contains {{bracket}}"
        self.assertTrue(Utils.is_containing_bracket(order_to_test),
                        "Fail returning True when order contains no spaced bracket")

        # Failure
        order_to_test = "This test does not contain bracket"
        self.assertFalse(Utils.is_containing_bracket(order_to_test),
                         "Fail returning False when order has no brackets")

        # Behaviour
        order_to_test = ""
        self.assertFalse(Utils.is_containing_bracket(order_to_test),
                         "Fail returning False when no order")

        # Behaviour int
        order_to_test = 6
        self.assertFalse(Utils.is_containing_bracket(order_to_test),
                         "Fail returning False when an int")

        # Behaviour unicode
        order_to_test = "j'aime les goûters l'été"
        self.assertFalse(Utils.is_containing_bracket(order_to_test),
                         "Fail returning False when an int")

    def test_get_next_value_list(self):
        # Success
        list_to_test = {1, 2, 3}
        self.assertEqual(Utils.get_next_value_list(list_to_test), 2,
                         "Fail to match the expected next value from the list")

        # Failure
        list_to_test = {1}
        self.assertEqual(Utils.get_next_value_list(list_to_test), None,
                         "Fail to ensure there is no next value from the list")

        # Behaviour
        list_to_test = {}
        self.assertEqual(Utils.get_next_value_list(list_to_test), None,
                         "Fail to ensure the empty list return None value")

    def test_find_all_matching_brackets(self):
        """
        Test the Utils find all matching brackets
        """
        sentence = "This is the {{bracket}}"
        expected_result = ["{{bracket}}"]
        self.assertEqual(Utils.find_all_matching_brackets(sentence=sentence),
                         expected_result,
                         "Fail to match one bracket")

        sentence = "This is the {{bracket}} {{second}}"
        expected_result = ["{{bracket}}", "{{second}}"]
        self.assertEqual(Utils.find_all_matching_brackets(sentence=sentence),
                         expected_result,
                         "Fail to match two brackets")

    def test_remove_spaces_in_brackets(self):
        """
        Test the Utils remove_spaces_in_brackets
        """

        sentence = "This is the {{ bracket   }}"
        expected_result = "This is the {{bracket}}"
        self.assertEqual(Utils.remove_spaces_in_brackets(sentence=sentence),
                         expected_result,
                         "Fail to remove spaces in one bracket")

        sentence = "This is the {{ bracket   }} {{  second     }}"
        expected_result = "This is the {{bracket}} {{second}}"
        self.assertEqual(Utils.remove_spaces_in_brackets(sentence=sentence),
                         expected_result,
                         "Fail to remove spaces in two brackets")

        # test with json
        sentence = "{\"params\": {\"apikey\": \"ISNOTMYPASSWORD\", " \
                   "\"query\": \"met le chauffage a {{ valeur }} degres\"}}"
        expected_result = "{\"params\": {\"apikey\": \"ISNOTMYPASSWORD\", " \
                          "\"query\": \"met le chauffage a {{valeur}} degres\"}}"
        self.assertEqual(Utils.remove_spaces_in_brackets(sentence=sentence),
                         expected_result,
                         "Fail to remove spaces in two brackets")

    def test_encode_text_utf8(self):
        """
        Test encoding the text in utf8
        """
        sentence = "kâllìöpé"
        if sys.version_info[0] < 3:
            sentence = sentence.decode('utf8')
        expected_sentence = "kâllìöpé"

        self.assertEqual(Utils.encode_text_utf8(text=sentence),
                         expected_sentence)


if __name__ == '__main__':
    unittest.main()
