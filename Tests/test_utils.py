import unittest
import os
import mock

from kalliope.core.Models.Neuron import Neuron
from kalliope.core.Models.Order import Order
from kalliope.core.Models.Synapse import Synapse
from kalliope.neurons.say.say import Say
from kalliope.core.Utils.Utils import Utils

from kalliope.core.ConfigurationManager import SettingLoader
from kalliope.core.ConfigurationManager import BrainLoader


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

        self.assertEquals(Utils.get_current_file_parent_path(path_to_test),
                          expected_result,
                          "fail getting the parent parent path from the given path")

    def test_get_current_file_parent_parent_path(self):
        """
        Expect to get back the parent parent path file
        """
        path_to_test = "../kalliope/core/Utils"
        expected_result = os.path.normpath("../kalliope")

        self.assertEquals(Utils.get_current_file_parent_parent_path(path_to_test),
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
        absolute_path_to_test = os.path.join(dir_path,file_name)
        expected_result = absolute_path_to_test
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        # touch the file
        open(absolute_path_to_test, 'a').close()

        self.assertEquals(Utils.get_real_file_path(absolute_path_to_test),
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

        self.assertEquals(Utils.get_real_file_path(file_name),
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
        expected_result = os.path.normpath(os.getcwd() + os.sep + os.pardir + os.sep +"kalliope" + os.sep + file_name)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        # touch the file
        open(path_to_test, 'a').close()

        self.assertEquals(Utils.get_real_file_path(file_name),
                          expected_result,
                          "Fail to match the /an/unknown/path/kalliope path")
        # Clean up
        if os.path.exists(file_name):
            os.remove(file_name)

    def test_get_dynamic_class_instantiation(self):
        """
        Test that an instance as been instantiate properly.
        """
        sl = SettingLoader()
        sl.settings.resource_dir = '/var/tmp/test/resources'

        neuron = Neuron(name='Say', parameters={'message': 'test dynamic class instantiate'})
        self.assertTrue(isinstance(Utils.get_dynamic_class_instantiation(package_name="neurons",
                                                                         module_name=neuron.name.capitalize(),
                                                                         parameters=neuron.parameters,
                                                                         resources_dir='/var/tmp/test/resources'),
                                   Say),
                        "Fail instantiate a class")

