import unittest
import os

from core.NeuronModule import MissingParameterException, InvalidParameterException
from neurons.script.script import Script
from core.FileManager import FileManager


class TestScript(unittest.TestCase):

    def setUp(self):
        self.path = "path"
        self.random = "random"

    def testParameters(self):
        def run_test_missing_param(parameters_to_test):
            with self.assertRaises(MissingParameterException):
                Script(**parameters_to_test)

        def run_test_invalid_param(parameters_to_test):
            with self.assertRaises(InvalidParameterException):
                Script(**parameters_to_test)

        # empty
        parameters = dict()
        run_test_missing_param(parameters)

        # missing path
        parameters = {
            "random": self.random
        }
        run_test_missing_param(parameters)

        # random path
        self.path = "/tmp/iamarandompath/anotherrandompath/kalliope"
        parameters = {
            "path": self.path
        }
        run_test_invalid_param(parameters)

        # Test Non executable file
        # Create the file and remove permissions to the user
        tmp_path = "/tmp/kalliope/tests/"
        tmp_file_path = tmp_path+"neuronScript"
        if not os.path.exists(tmp_path):
            os.makedirs(tmp_path)
        FileManager.write_in_file(tmp_file_path, "[kalliope-test] TestScript - testParameters")
        os.chmod(tmp_file_path, 0600)
        # test the user does not have access
        self.path = tmp_file_path
        parameters = {
            "path": self.path
        }
        run_test_invalid_param(parameters)
        # Remove the tmp file
        os.chmod(tmp_file_path, 0700)
        FileManager.remove_file(tmp_file_path)


if __name__ == '__main__':
    unittest.main()
