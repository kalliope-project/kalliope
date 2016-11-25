import unittest

from core.NeuronModule import MissingParameterException
from neurons.openweathermap.openweathermap import Openweathermap


class TestOpenWeatherMap(unittest.TestCase):

    def setUp(self):
        self.location="location"
        self.api_key="api_key"

    def testParameters(self):
        def run_test(parameters_to_test):
            with self.assertRaises(MissingParameterException):
                Openweathermap(**parameters_to_test)

        # empty
        parameters = dict()
        run_test(parameters)

        # missing api_key
        parameters = {
            "location": self.location
        }
        run_test(parameters)

        # missing location
        parameters = {
           "api_key": self.api_key
        }
        run_test(parameters)


if __name__ == '__main__':
    unittest.main()
