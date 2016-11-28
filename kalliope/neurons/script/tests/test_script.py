import os
import time
import unittest

from kalliope.core.NeuronModule import MissingParameterException, InvalidParameterException
from kalliope.neurons.script.script import Script


class TestScript(unittest.TestCase):

    def setUp(self):
        self.path = "path"
        self.random = "random"
        self.test_file = "/tmp/kalliope_text_shell.txt"

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
        text_to_write = "[kalliope-test] TestScript - testParameters"
        with open(tmp_file_path, 'w') as myFile:
            myFile.write(text_to_write)
        os.chmod(tmp_file_path, 0600)
        # test the user does not have access
        self.path = tmp_file_path
        parameters = {
            "path": self.path
        }
        run_test_invalid_param(parameters)
        # Remove the tmp file
        os.chmod(tmp_file_path, 0700)
        os.remove(tmp_file_path)

    def test_script_execution(self):
        """
        Test we can run a script
        """
        param = {
            "path": "kalliope/neurons/script/tests/test_script.sh"
        }

        Script(**param)
        self.assertTrue(os.path.isfile(self.test_file))

        # remove the tet file
        os.remove(self.test_file)

    def test_script_execution_async(self):
        """
        Test we can run a script asynchronously
        """
        param = {
            "path": "kalliope/neurons/script/tests/test_script.sh",
            "async": True
        }

        Script(**param)
        # let the time to the thread to do its job
        time.sleep(0.5)
        self.assertTrue(os.path.isfile(self.test_file))

        # remove the test file
        os.remove(self.test_file)

    def test_script_content(self):
        """
        Test we can get a content from the launched script
        """
        text_to_write = 'kalliope'
        # we write a content into a file
        with open(self.test_file, 'w') as myFile:
            myFile.write(text_to_write)

        # get the output with the neuron
        parameters = {
            "path": "kalliope/neurons/script/tests/test_script_cat.sh",
        }

        script = Script(**parameters)
        self.assertEqual(script.output, text_to_write)
        self.assertEqual(script.returncode, 0)

        # remove the tet file
        os.remove(self.test_file)

if __name__ == '__main__':
    unittest.main()
