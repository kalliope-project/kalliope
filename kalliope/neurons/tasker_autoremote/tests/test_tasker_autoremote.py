import unittest

from core.NeuronModule import MissingParameterException
from neurons.sleep.sleep import Sleep


class TestSleep(unittest.TestCase):

    def setUp(self):
        self.key="key"
        self.message="message"

    def testParameters(self):
        def run_test(parameters_to_test):
            with self.assertRaises(MissingParameterException):
                Sleep(**parameters_to_test)

        # empty
        parameters = dict()
        run_test(parameters)

        # missing key
        parameters = {
            "message": self.message
        }
        run_test(parameters)

        # missing message
        parameters = {
            "key": self.key
        }
        run_test(parameters)


if __name__ == '__main__':
    unittest.main()
