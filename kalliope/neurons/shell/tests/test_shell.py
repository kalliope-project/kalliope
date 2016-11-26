import os
import unittest

import time

from kalliope.core.NeuronModule import MissingParameterException
from kalliope.neurons.shell.shell import Shell


class TestShell(unittest.TestCase):

    def setUp(self):
        self.cmd = "cmd"
        self.random = "random"
        self.test_file = "/tmp/kalliope_text_shell.txt"

    def testParameters(self):
        def run_test(parameters_to_test):
            with self.assertRaises(MissingParameterException):
                Shell(**parameters_to_test)

        # empty
        parameters = dict()
        run_test(parameters)

        # missing cmd
        parameters = {
            "random": self.random
        }
        run_test(parameters)

    def test_shell_returned_code(self):
        """
        To test that the shell neuron works, we ask it to create a file
        """
        parameters = {
            "cmd": "touch %s" % self.test_file
        }

        shell = Shell(**parameters)
        self.assertTrue(os.path.isfile(self.test_file))
        self.assertEqual(shell.returncode, 0)
        # remove the test file
        os.remove(self.test_file)

    def test_shell_content(self):
        """
        Test we can get a content from the launched command
        """
        text_to_write = 'kalliope'
        # we write a content into a file
        with open(self.test_file, 'w') as myFile:
            myFile.write(text_to_write)

        # get the output with the neuron
        parameters = {
            "cmd": "cat %s" % self.test_file
        }

        shell = Shell(**parameters)
        self.assertEqual(shell.output, text_to_write)
        self.assertEqual(shell.returncode, 0)
        # remove the test file
        os.remove(self.test_file)

    def test_async_shell(self):
        """
        Test that the neuron can run a shell command asynchronously
        """
        parameters = {
            "cmd": "touch %s" % self.test_file,
            "async": True
        }

        Shell(**parameters)
        # let the time the the thread to perform the action
        time.sleep(0.5)
        self.assertTrue(os.path.isfile(self.test_file))
        # remove the test file
        os.remove(self.test_file)


if __name__ == '__main__':
    unittest.main()
