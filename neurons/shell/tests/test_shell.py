import unittest

from core.NeuronModule import MissingParameterException
from neurons.shell.shell import Shell


class TestShell(unittest.TestCase):

    def setUp(self):
        self.cmd="cmd"
        self.random="random"

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


if __name__ == '__main__':
    unittest.main()
