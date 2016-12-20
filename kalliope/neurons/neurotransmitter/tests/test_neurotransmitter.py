import unittest

from mock import mock

from kalliope.core.NeuronModule import NeuronModule, MissingParameterException, InvalidParameterException
from kalliope.neurons.neurotransmitter import Neurotransmitter


class TestNeurotransmitter(unittest.TestCase):

    def setUp(self):
        self.from_answer_link = [
            {
                "synapse": "synapse2",
                "answers": [
                    "answer one"
                ]
            },
            {
                "synapse": "synapse3",
                "answers": [
                    "answer two",
                    "answer three"
                ]
            },
        ]
        self.direct_link = "direct_link"
        self.default = "default"

    def testParameters(self):
        """
        Testing the Parameters checking
        """
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
        """
        Testing the callback provided when audio has been provided by the User as an answer.
        """
        parameters = {
            "default": self.default,
            "from_answer_link": self.from_answer_link
        }
        with mock.patch.object(NeuronModule, 'get_audio_from_stt', create=True) as mock_get_audio_from_stt:
            with mock.patch.object(NeuronModule, 'run_synapse_by_name', create=True) as mock_run_synapse_by_name:
                # testing running the default when no order matching
                nt = Neurotransmitter(**parameters)
                mock_get_audio_from_stt.assert_called_once()
                mock_get_audio_from_stt.reset_mock()
                # testing running the default when audio None
                audio_text = None
                nt.callback(audio=audio_text)
                mock_run_synapse_by_name.assert_called_once_with(self.default)
                mock_run_synapse_by_name.reset_mock()
                # testing running the default when no order matching
                audio_text = "try test audio "
                nt.callback(audio=audio_text)
                mock_run_synapse_by_name.assert_called_once_with(self.default)
                mock_run_synapse_by_name.reset_mock()

                with mock.patch.object(NeuronModule,
                                       'run_synapse_by_name_with_order',
                                       create=True) as mock_run_synapse_by_name_with_order:

                    audio_text="answer one"
                    nt.callback(audio=audio_text)
                    mock_run_synapse_by_name_with_order.assert_called_once_with(order=audio_text,
                                                                                synapse_name="synapse2",
                                                                                order_template="answer one")

    def testInit(self):
        """
        Testing the init method of the neurontransmitter.
        """

        with mock.patch.object(NeuronModule, 'run_synapse_by_name', create=True) as mock_run_synapse_by_name:
            # Test direct link
            parameters = {
                "default": self.default,
                "direct_link": self.direct_link
            }
            nt = Neurotransmitter(**parameters)
            mock_run_synapse_by_name.assert_called_once_with(self.direct_link)

        with mock.patch.object(NeuronModule, 'get_audio_from_stt', create=True) as mock_get_audio_from_stt:
            # Test get_audio_from_stt
            parameters = {
                "default": self.default,
                "from_answer_link": self.from_answer_link,
            }
            nt = Neurotransmitter(**parameters)
            mock_get_audio_from_stt.assert_called_once()





