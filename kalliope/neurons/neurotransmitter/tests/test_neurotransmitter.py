import unittest

from kalliope.core.NeuronModule import MissingParameterException, InvalidParameterException
from kalliope.neurons.neurotransmitter import Neurotransmitter


class TestNeurotransmitter(unittest.TestCase):

    def setUp(self):
        self.from_answer_link = [
            {
                "synapse": "synapse2",
                "answer": "blabla"
            },
            {
                "synapse": "synapse3",
                "answer": "blablablbla",
                "answer": "blablblobloa",
            },
        ]
        self.direct_link = "direct_link"
        self.default = "default"

    def testParameters(self):
        def run_test_InvalidParameterException(parameters_to_test):
            with self.assertRaises(InvalidParameterException):
                Neurotransmitter(**parameters_to_test)

        def run_test_MissingParameterException(parameters_to_test):
            with self.assertRaises(MissingParameterException):
                Neurotransmitter(**parameters_to_test)

        # empty
        parameters = dict()
        run_test_MissingParameterException(parameters)

        # missing direct_link and from_answer_link
        parameters = {
            "default": self.default
        }
        run_test_MissingParameterException(parameters)

        # missing direct_link and from_answer_link
        parameters = {
            "default": self.default,
            "from_answer_link": self.from_answer_link,
            "direct_link": self.direct_link
        }
        run_test_InvalidParameterException(parameters)

        # missing default
        parameters = {
            "from_answer_link": self.from_answer_link,
            "direct_link": self.direct_link
        }
        run_test_InvalidParameterException(parameters)

        # Missing answer in from_answer_link
        self.from_answer_link = [
            {
                "synapse": "synapse2",
            }
        ]

        parameters = {
            "default": self.default,
            "from_answer_link": self.from_answer_link
        }
        run_test_MissingParameterException(parameters)

        # Missing synapse in from_answer_link
        self.from_answer_link = [
            {
                "answer": "blablablbla",
            }
        ]

        parameters = {
            "default": self.default,
            "from_answer_link": self.from_answer_link
        }
        run_test_MissingParameterException(parameters)


    def testCallback(self):
        pass