import unittest

from kalliope.core.NeuronModule import MissingParameterException
from kalliope.neurons.sleep.sleep import Sleep


class TestSleep(unittest.TestCase):

    def setUp(self):
        self.seconds = 10
        self.random="random"

    def testParameters(self):
        def run_test(parameters_to_test):
            with self.assertRaises(MissingParameterException):
                Sleep(**parameters_to_test)

        # empty
        parameters = dict()
        run_test(parameters)

        # missing seconds
        parameters = {
            "random": self.random
        }
        run_test(parameters)


if __name__ == '__main__':
    unittest.main()
