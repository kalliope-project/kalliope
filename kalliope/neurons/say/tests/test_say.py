import unittest
from unittest import mock

from kalliope import SynapseLauncher
from kalliope.core.Models import Synapse, Neuron, Signal, Brain
from kalliope.core.NeuronModule import MissingParameterException
from kalliope.neurons.say.say import Say


class TestSay(unittest.TestCase):

    def setUp(self):
        self.message = "message"
        self.random = "random"

    def testParameters(self):
        def run_test(parameters_to_test):
            with self.assertRaises(MissingParameterException):
                Say(**parameters_to_test)

        # empty
        parameters = dict()
        run_test(parameters)

        # missing message
        parameters = {
            "random": self.random
        }
        run_test(parameters)

    def test_say(self):
        # single message
        parameters = {
            "message": "test message"
        }
        with mock.patch("kalliope.tts.pico2wave.Pico2wave.say") as mock_tts:
            Say(**parameters)
            mock_tts.assert_called_once_with("test message")

        # template
        parameters = {
            "file_template": "test_say_neuron_template.j2"
        }
        with mock.patch("kalliope.tts.pico2wave.Pico2wave.say") as mock_tts:
            Say(**parameters)
            mock_tts.assert_called_once_with("hello sir")

    def test_synapse_with_say(self):
        neuron1 = Neuron(name='say', parameters={'message': 'I say hello to {{ variable }}'})
        signal1 = Signal(name="order", parameters="hello {{ variable }}")
        synapse1 = Synapse(name="Synapse1", neurons=[neuron1], signals=[signal1])

        all_synapse_list = [synapse1]
        brain_test = Brain(synapses=all_synapse_list)
        with mock.patch("kalliope.tts.pico2wave.Pico2wave.say") as mock_tts:
            SynapseLauncher.run_matching_synapse_from_order(order_to_process="hello world",
                                                            brain=brain_test,
                                                            settings=None)
            mock_tts.assert_called_once_with("I say hello to world")

    def test_synapse_with_say_and_template(self):
        neuron1 = Neuron(name='say', parameters={'file_template': 'test_say_neuron_template_with_variable.j2',
                                                 'parameters': {"variable": "{{ variable }}"}})
        signal1 = Signal(name="order", parameters="hello {{ variable }}")
        synapse1 = Synapse(name="Synapse1", neurons=[neuron1], signals=[signal1])
        all_synapse_list = [synapse1]
        brain_test = Brain(synapses=all_synapse_list)
        with mock.patch("kalliope.tts.pico2wave.Pico2wave.say") as mock_tts:
            SynapseLauncher.run_matching_synapse_from_order(order_to_process="hello world",
                                                            brain=brain_test,
                                                            settings=None)
            mock_tts.assert_called_once_with("I say hello to world")
