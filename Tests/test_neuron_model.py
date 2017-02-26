import os
import unittest

from kalliope.core.Models import Neuron


class TestNeuronModule(unittest.TestCase):

    def test_password_parameter(self):
        neuron_name = "test"
        neuron_parameters = {
            "password": "my secret",
            "parameter": "test"
        }

        neuron = Neuron()
        neuron.name = neuron_name
        neuron.parameters = neuron_parameters

        print neuron.__str__()
        expected_result = "Neuron: name: test, parameters: {'password': '*****', 'parameter': 'test'}"

        self.assertEqual(neuron.__str__(), expected_result)

    def test_password_in_parameter(self):
        neuron_name = "test"
        neuron_parameters = {
            "password_parameter": "my secret",
            "parameter": "test"
        }

        neuron = Neuron()
        neuron.name = neuron_name
        neuron.parameters = neuron_parameters

        print neuron.__str__()
        expected_result = "Neuron: name: test, parameters: {'parameter': 'test', 'password_parameter': '*****'}"

        self.assertEqual(neuron.__str__(), expected_result)

if __name__ == '__main__':
    unittest.main()
