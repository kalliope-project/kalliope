import unittest

import mock

from kalliope.core.NeuronModule import MissingParameterException
from kalliope.neurons.brain.brain import Brain


class TestBrain(unittest.TestCase):

    def test_is_parameters_ok(self):
        # valid neuron with boolean
        synapse_name = "synapse_name"
        enabled = True
        with mock.patch("kalliope.neurons.brain.brain.Brain._update_brain"):
            brain_neuron = Brain(synapse_name=synapse_name, enabled=enabled)
            self.assertTrue(brain_neuron._is_parameters_ok())
            self.assertTrue(brain_neuron.enabled)

        # valid neuron with boolean as string
        synapse_name = "synapse_name"
        enabled = "True"
        with mock.patch("kalliope.neurons.brain.brain.Brain._update_brain"):
            brain_neuron = Brain(synapse_name=synapse_name, enabled=enabled)
            self.assertTrue(brain_neuron._is_parameters_ok())
            self.assertTrue(brain_neuron.enabled)

        # valid neuron with boolean as string
        synapse_name = "synapse_name"
        enabled = "true"
        with mock.patch("kalliope.neurons.brain.brain.Brain._update_brain"):
            brain_neuron = Brain(synapse_name=synapse_name, enabled=enabled)
            self.assertTrue(brain_neuron._is_parameters_ok())
            self.assertTrue(brain_neuron.enabled)

        # invalid neuron with no synapse name
        synapse_name = ""
        enabled = "true"
        with mock.patch("kalliope.neurons.brain.brain.Brain._update_brain"):
            with self.assertRaises(MissingParameterException):
                Brain(synapse_name=synapse_name, enabled=enabled)

        # invalid neuron with no synapse name
        synapse_name = "test"
        enabled = ""
        with mock.patch("kalliope.neurons.brain.brain.Brain._update_brain"):
            with self.assertRaises(MissingParameterException):
                Brain(synapse_name=synapse_name, enabled=enabled)

        # valid neuron but enabled bool automatically converted to False
        synapse_name = "test"
        enabled = "no a bool"
        with mock.patch("kalliope.neurons.brain.brain.Brain._update_brain"):
            brain_neuron = Brain(synapse_name=synapse_name, enabled=enabled)
            self.assertTrue(brain_neuron._is_parameters_ok())
            self.assertFalse(brain_neuron.enabled)


if __name__ == '__main__':
    unittest.main()
