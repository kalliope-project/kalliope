import unittest

from core.NeuronModule import MissingParameterException
from neurons.gmail_checker.gmail_checker import Gmail_checker


class TestGmail_Checker(unittest.TestCase):

    def setUp(self):
        self.username="username"
        self.password="password"

    def testParameters(self):
        def run_test(parameters_to_test):
            with self.assertRaises(MissingParameterException):
                Gmail_checker(**parameters_to_test)

        # empty
        parameters = dict()
        run_test(parameters)

        # missing password
        parameters = {
            "username": self.username
        }
        run_test(parameters)

        # missing username
        parameters = {
           "password": self.password
        }
        run_test(parameters)

