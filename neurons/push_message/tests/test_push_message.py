import unittest

from core.NeuronModule import MissingParameterException
from neurons.push_message.push_message import Push_message


class TestPush_Message(unittest.TestCase):

    def setUp(self):
        self.message="message"
        self.api_key="api_key"
        self.channel_name = "channel_name"

    def testParameters(self):
        def run_test(parameters_to_test):
            with self.assertRaises(MissingParameterException):
                Push_message(**parameters_to_test)

        # empty
        parameters = dict()
        run_test(parameters)

        # missing api_key
        parameters = {
            "message": self.message,
            "channel_name": self.channel_name
        }
        run_test(parameters)

        # missing channel_name
        parameters = {
           "api_key": self.api_key,
            "message":self.message
        }
        run_test(parameters)

        # missing message
        parameters = {
            "api_key": self.api_key,
            "channel_name": self.channel_name
        }
        run_test(parameters)


if __name__ == '__main__':
    unittest.main()
