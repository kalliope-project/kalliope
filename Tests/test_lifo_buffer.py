import os
import unittest

import mock

from kalliope.core import LifoManager
from kalliope.core.ConfigurationManager import BrainLoader
from kalliope.core.Lifo.LIFOBuffer import Serialize, SynapseListAddedToLIFO

from kalliope.core.Models import Singleton
from kalliope.core.Models.MatchedSynapse import MatchedSynapse


class TestLIFOBuffer(unittest.TestCase):

    def setUp(self):
        # be sure the brain haven't been instantiated before
        Singleton._instances = dict()

        if "/Tests" in os.getcwd():
            self.brain_to_test = os.getcwd() + os.sep + "brains/lifo_buffer_test_brain.yml"
        else:
            self.brain_to_test = os.getcwd() + os.sep + "Tests/brains/lifo_buffer_test_brain.yml"

        BrainLoader(file_path=self.brain_to_test)
        # create a new lifo buffer
        self.lifo_buffer = LifoManager.get_singleton_lifo()
        self.lifo_buffer.clean()

    def test_execute(self):
        """
        In this test the brain contains a neurotransmitter
        """
        # --------------------------------------
        # Test 1. The user answers correctly to all neurotransmitter
        # --------------------------------------

        # we suppose that the first synapse has matched the first synapse
        synapse = BrainLoader().brain.get_synapse_by_name("synapse1")
        order = "enter in synapse 1"
        matched_synapse = MatchedSynapse(matched_synapse=synapse,
                                         user_order=order,
                                         matched_order=order)
        list_matched_synapse = list()
        list_matched_synapse.append(matched_synapse)
        self.lifo_buffer.add_synapse_list_to_lifo(list_matched_synapse)
        self.lifo_buffer.api_response.user_order = order

        with mock.patch("kalliope.core.TTS.TTSModule.generate_and_play"):

            response = self.lifo_buffer.execute(is_api_call=True)

            expected_result = {
                'status': 'waiting_for_answer',
                'matched_synapses': [
                    {
                        'matched_order': 'enter in synapse 1',
                        'neuron_module_list':
                            [
                                {
                                    'neuron_name': 'Say',
                                    'generated_message': 'question in synapse 1'
                                }
                            ],
                        'synapse_name': 'synapse1'
                    }
                ],
                'user_order': 'enter in synapse 1'
            }

            self.assertEqual(response, expected_result)

            # give an answer
            answer = "answer synapse1"
            response = self.lifo_buffer.execute(answer=answer,
                                                is_api_call=True)
            expected_result = {
                'status': 'waiting_for_answer',
                'matched_synapses': [
                    {
                        'matched_order': 'enter in synapse 1',
                        'neuron_module_list': [
                            {
                                'neuron_name': 'Say',
                                'generated_message': 'question in synapse 1'
                            },
                            {
                                'neuron_name': 'Neurotransmitter',
                                'generated_message': None
                            }
                        ],
                        'synapse_name': 'synapse1'
                    },
                    {
                        'matched_order': 'answer synapse1',
                        'neuron_module_list': [
                            {
                                'neuron_name': 'Say',
                                'generated_message': 'enter synapse 2'
                            }
                        ],
                        'synapse_name': 'synapse2'
                    }
                ],
                'user_order': None
            }
            self.assertEqual(response, expected_result)

            # give the last answer
            answer = "synapse5"
            response = self.lifo_buffer.execute(answer=answer,
                                                is_api_call=True)
            expected_result = {
                'status': 'complete',
                'matched_synapses': [
                    {
                        'matched_order': 'answer synapse1',
                        'neuron_module_list': [
                            {
                                'neuron_name': 'Say',
                                'generated_message': 'enter synapse 2'
                            },
                            {
                                'neuron_name': 'Neurotransmitter',
                                'generated_message': None
                            }
                        ],
                        'synapse_name': 'synapse2'
                    },
                    {
                        'matched_order': 'synapse5',
                        'neuron_module_list': [
                            {
                                'neuron_name': 'Say',
                                'generated_message': 'execution of synapse 5'
                            }
                        ],
                        'synapse_name': 'synapse5'
                    },
                    {
                        'matched_order': 'enter in synapse 1',
                        'neuron_module_list': [
                            {
                                'neuron_name': 'Say',
                                'generated_message': 'question in synapse 1'
                            },
                            {
                                'neuron_name': 'Neurotransmitter',
                                'generated_message': None
                            },
                            {
                                'neuron_name': 'Say',
                                'generated_message': 'last neuron in synapse 1'
                            }
                        ],
                        'synapse_name': 'synapse1'
                    }
                ],
                'user_order': None
            }

            self.assertEqual(response, expected_result)

        # --------------------------------------
        # Test 2. The user doesn't answered correctly to the first neurotransmitter
        # --------------------------------------

        # we suppose that the first synapse has matched the first synapse
        synapse = BrainLoader().brain.get_synapse_by_name("synapse1")
        order = "enter in synapse 1"
        matched_synapse = MatchedSynapse(matched_synapse=synapse,
                                         user_order=order,
                                         matched_order=order)
        list_matched_synapse = list()
        list_matched_synapse.append(matched_synapse)
        self.lifo_buffer.add_synapse_list_to_lifo(list_matched_synapse)
        self.lifo_buffer.api_response.user_order = order

        with mock.patch("kalliope.core.TTS.TTSModule.generate_and_play"):
            # fist call to enter in the neurotransmitter
            self.lifo_buffer.execute(is_api_call=True)

            wrong_answer = "wrong answer"
            response = self.lifo_buffer.execute(answer=wrong_answer, is_api_call=True)

            expected_result = {
                'status': 'complete',
                'matched_synapses': [
                    {
                        'matched_order': 'enter in synapse 1',
                        'neuron_module_list': [
                            {
                                'neuron_name': 'Say',
                                'generated_message': 'question in synapse 1'
                            },
                            {
                                'neuron_name': 'Neurotransmitter',
                                'generated_message': None
                            },
                            {
                                'neuron_name': 'Say',
                                'generated_message': 'last neuron in synapse 1'
                            }
                        ],
                        'synapse_name': 'synapse1'
                    },
                    {
                        'matched_order': None,
                        'neuron_module_list': [
                            {
                                'neuron_name': 'Say',
                                'generated_message': 'not understood'
                            }
                        ],
                        'synapse_name': 'synapse4'
                    }
                ],
                'user_order': None
            }

            self.assertEqual(response, expected_result)

        # --------------------------------------
        # Test 3. No synapse matched, we still execute the list
        # --------------------------------------
        list_matched_synapse = list()
        self.lifo_buffer.add_synapse_list_to_lifo(list_matched_synapse)
        self.lifo_buffer.api_response.user_order = "this is an order"

        with mock.patch("kalliope.core.TTS.TTSModule.generate_and_play"):
            # fist call to enter in the neurotransmitter
            response = self.lifo_buffer.execute(is_api_call=True)

            expected_result = {
                'status': None,
                'matched_synapses': [],
                'user_order': 'this is an order'
            }

            self.assertEqual(response, expected_result)

    def test_add_synapse_list_to_lifo(self):
        """
        Testing to add a synapse to the lifo
        """
        synapse = BrainLoader().brain.get_synapse_by_name("synapse1")
        order = "enter in synapse 1"
        matched_synapse = MatchedSynapse(matched_synapse=synapse,
                                         user_order=order,
                                         matched_order=order)
        list_matched_synapse = list()
        list_matched_synapse.append(matched_synapse)
        self.lifo_buffer.add_synapse_list_to_lifo(list_matched_synapse)

        self.assertEqual(self.lifo_buffer.lifo_list, [list_matched_synapse])

    def test_clean(self):
        """
        Test the Cleaning of the matched synapses list
        """
        synapse = BrainLoader().brain.get_synapse_by_name("synapse1")
        order = "enter in synapse 1"
        matched_synapse = MatchedSynapse(matched_synapse=synapse,
                                         user_order=order,
                                         matched_order=order)
        list_matched_synapse = list()
        list_matched_synapse.append(matched_synapse)
        self.lifo_buffer.add_synapse_list_to_lifo(list_matched_synapse)

        self.lifo_buffer.clean()
        self.assertEqual(0, len(self.lifo_buffer.lifo_list))

    def test_return_serialized_api_response(self):
        """
        Test the serialization
        """
        self.lifo_buffer.clean()
        self.lifo_buffer.execute(is_api_call=True)
        expected_result = {'status': None, 'matched_synapses': [], 'user_order': None}
        response = self.lifo_buffer._return_serialized_api_response()
        self.assertEqual(expected_result, response)

    def test_process_synapse_list(self):
        """
        Testing the neuron list from a synapse
        """
        synapse = BrainLoader().brain.get_synapse_by_name("synapse1")
        order = "enter in synapse 1"
        matched_synapse = MatchedSynapse(matched_synapse=synapse,
                                         user_order=order,
                                         matched_order=order)
        list_matched_synapse = list()
        list_matched_synapse.append(matched_synapse)

        with mock.patch("kalliope.core.Lifo.LIFOBuffer._process_neuron_list"):
            self.lifo_buffer._process_synapse_list(list_matched_synapse)
            expected_response = {
                'status': None,
                'matched_synapses': [
                    {
                        'matched_order': 'enter in synapse 1',
                        'neuron_module_list': [],
                        'synapse_name': 'synapse1'
                    }
                ],
                'user_order': None
            }
            self.assertEqual(expected_response, self.lifo_buffer.api_response.serialize())
            self.assertEqual(0, len(self.lifo_buffer.lifo_list))

    def test_process_neuron_list(self):
        # Test with a neuron that doesn't wait for an answer
        synapse = BrainLoader().brain.get_synapse_by_name("synapse5")
        order = "synapse5"
        matched_synapse = MatchedSynapse(matched_synapse=synapse,
                                         user_order=order,
                                         matched_order=order)

        with mock.patch("kalliope.core.TTS.TTSModule.generate_and_play"):
            self.lifo_buffer.set_api_call(True)
            self.lifo_buffer._process_neuron_list(matched_synapse=matched_synapse)
            self.assertEqual("complete", self.lifo_buffer.api_response.status)

        # test with neuron that wait for an answer
        LifoManager.clean_saved_lifo()
        synapse = BrainLoader().brain.get_synapse_by_name("synapse6")
        order = "synapse6"
        matched_synapse = MatchedSynapse(matched_synapse=synapse,
                                         user_order=order,
                                         matched_order=order)

        self.lifo_buffer.set_api_call(True)
        with mock.patch("kalliope.core.TTS.TTSModule.generate_and_play"):
            with self.assertRaises(Serialize):
                self.lifo_buffer._process_neuron_list(matched_synapse=matched_synapse)

        # test with a neuron that want to add a synapse list to the LIFO
        LifoManager.clean_saved_lifo()
        synapse = BrainLoader().brain.get_synapse_by_name("synapse6")
        order = "synapse6"
        matched_synapse = MatchedSynapse(matched_synapse=synapse,
                                         user_order=order,
                                         matched_order=order)

        self.lifo_buffer.set_api_call(True)
        self.lifo_buffer.set_answer("synapse 6 answer")
        with mock.patch("kalliope.core.TTS.TTSModule.generate_and_play"):
            self.assertRaises(SynapseListAddedToLIFO,
                              self.lifo_buffer._process_neuron_list(matched_synapse=matched_synapse))


if __name__ == '__main__':
    unittest.main()

    # suite = unittest.TestSuite()
    # suite.addTest(TestLIFOBuffer("test_execute"))
    # runner = unittest.TextTestRunner()
    # runner.run(suite)
