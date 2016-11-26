import unittest
import ipaddress

from kalliope.core.NeuronModule import InvalidParameterException, MissingParameterException
from kalliope.neurons.wake_on_lan.wake_on_lan import Wake_on_lan


class TestWakeOnLan(unittest.TestCase):

    def setUp(self):
        self.mac_address="00:0a:95:9d:68:16"
        self.broadcast_address = "255.255.255.255"
        self.port = 42

    def testParameters(self):
        def run_test_invalidParam(parameters_to_test):
            with self.assertRaises(InvalidParameterException):
                Wake_on_lan(**parameters_to_test)

        def run_test_missingParam(parameters_to_test):
            with self.assertRaises(MissingParameterException):
                Wake_on_lan(**parameters_to_test)

        def run_test_valueError(parameters_to_test):
            with self.assertRaises(ValueError):
                Wake_on_lan(**parameters_to_test)

        # empty
        parameters = dict()
        run_test_missingParam(parameters)

        # missing mac_address
        parameters = {
            "broadcast_address": self.broadcast_address,
            "port": self.port
        }
        run_test_missingParam(parameters)

        # port is not an int
        self.port = "port"
        parameters = {
            "broadcast_address": self.broadcast_address,
            "mac_address": self.mac_address,
            "port": self.port
        }
        run_test_invalidParam(parameters)
        self.port = 42

        # is broadcast not a valid format
        self.broadcast_address = "broadcast"
        parameters = {
            "broadcast_address": self.broadcast_address,
            "mac_address": self.mac_address,
            "port": self.port
        }
        run_test_valueError(parameters)
        self.broadcast_address = "255.255.255.255"

        # is mac_address not a valid IPv4 or IPv6 format
        self.mac_address = "mac_address"
        parameters = {
            "broadcast_address": self.broadcast_address,
            "mac_address": self.mac_address,
            "port": self.port
        }
        run_test_valueError(parameters)
        self.mac_address = "00:0a:95:9d:68:16"
