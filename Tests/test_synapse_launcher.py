import unittest

import mock

from kalliope.core import LifoManager
from kalliope.core.Models import Brain, Signal, Singleton
from kalliope.core.Models.MatchedSynapse import MatchedSynapse
from kalliope.core.Models.settings.Settings import Settings
from kalliope.core.SynapseLauncher import SynapseLauncher, SynapseNameNotFound

from kalliope.core.Models import Neuron
from kalliope.core.Models import Synapse


class TestSynapseLauncher(unittest.TestCase):
    """
    Test the class SynapseLauncher
    """

    def setUp(self):
        # Init
        neuron1 = Neuron(name='neurone1', parameters={'var1': 'val1'})
        neuron2 = Neuron(name='neurone2', parameters={'var2': 'val2'})
        neuron3 = Neuron(name='neurone3', parameters={'var3': 'val3'})
        neuron4 = Neuron(name='neurone4', parameters={'var4': 'val4'})

        signal1 = Signal(name="order", parameters="this is the sentence")
        signal2 = Signal(name="order", parameters="this is the second sentence")
        signal3 = Signal(name="order", parameters="that is part of the third sentence")

        self.synapse1 = Synapse(name="Synapse1", neurons=[neuron1, neuron2], signals=[signal1])
        self.synapse2 = Synapse(name="Synapse2", neurons=[neuron3, neuron4], signals=[signal2])
        self.synapse3 = Synapse(name="Synapse3", neurons=[neuron2, neuron4], signals=[signal3])

        self.all_synapse_list = [self.synapse1,
                                 self.synapse2,
                                 self.synapse3]

        self.brain_test = Brain(synapses=self.all_synapse_list)
        self.settings_test = Settings()

        # clean the LiFO
        Singleton._instances = dict()
        LifoManager.clean_saved_lifo()

    def test_start_synapse_by_list_name_single_synapse(self):
        # existing synapse in the brain
        with mock.patch("kalliope.core.Lifo.LIFOBuffer.execute"):
            should_be_created_matched_synapse = MatchedSynapse(matched_synapse=self.synapse1)
            SynapseLauncher.start_synapse_by_list_name(["Synapse1"], brain=self.brain_test)
            # we expect that the lifo has been loaded with the synapse to run
            expected_result = [[should_be_created_matched_synapse]]
            lifo_buffer = LifoManager.get_singleton_lifo()
            self.assertEqual(expected_result, lifo_buffer.lifo_list)

            # we expect that the lifo has been loaded with the synapse to run and overwritten parameters
            Singleton._instances = dict()
            LifoManager.clean_saved_lifo()
            lifo_buffer = LifoManager.get_singleton_lifo()
            overriding_param = {
                "val1": "val"
            }
            SynapseLauncher.start_synapse_by_list_name(["Synapse1"], brain=self.brain_test,
                                                       overriding_parameter_dict=overriding_param)
            should_be_created_matched_synapse = MatchedSynapse(matched_synapse=self.synapse1,
                                                               overriding_parameter=overriding_param)
            # we expect that the lifo has been loaded with the synapse to run
            expected_result = [[should_be_created_matched_synapse]]
            self.assertEqual(expected_result, lifo_buffer.lifo_list)

        # non existing synapse in the brain
        with self.assertRaises(SynapseNameNotFound):
            SynapseLauncher.start_synapse_by_list_name(["not_existing"], brain=self.brain_test)

        # check that the cortex is well loaded with temp parameter from a signal
        with mock.patch("kalliope.core.Lifo.LIFOBuffer.execute"):
            overriding_parameter_dict = {
                "parameter1": "value1"
            }
            with mock.patch("kalliope.core.Cortex.Cortex.add_parameters_from_order") as cortex_mock:
                SynapseLauncher.start_synapse_by_list_name(["Synapse1"],
                                                           brain=self.brain_test,
                                                           overriding_parameter_dict=overriding_parameter_dict)
                cortex_mock.assert_called_with(overriding_parameter_dict)

    def test_start_synapse_by_list_name(self):
        # test to start a list of synapse
        with mock.patch("kalliope.core.Lifo.LIFOBuffer.execute"):
            created_matched_synapse1 = MatchedSynapse(matched_synapse=self.synapse1)
            created_matched_synapse2 = MatchedSynapse(matched_synapse=self.synapse2)

            expected_list_matched_synapse = [created_matched_synapse1, created_matched_synapse2]

            SynapseLauncher.start_synapse_by_list_name(["Synapse1", "Synapse2"], brain=self.brain_test)
            # we expect that the lifo has been loaded with the synapse to run
            expected_result = [expected_list_matched_synapse]
            lifo_buffer = LifoManager.get_singleton_lifo()
            self.maxDiff = None
            self.assertEqual(expected_result, lifo_buffer.lifo_list)

        # empty list should return none
        empty_list = list()
        self.assertIsNone(SynapseLauncher.start_synapse_by_list_name(empty_list))

        # test to start a synapse list with a new lifo
        # we create a Lifo that is the current singleton
        Singleton._instances = dict()
        LifoManager.clean_saved_lifo()
        lifo_buffer = LifoManager.get_singleton_lifo()
        created_matched_synapse1 = MatchedSynapse(matched_synapse=self.synapse1)

        lifo_buffer.lifo_list = [created_matched_synapse1]
        # the current status of the singleton lifo should not move even after the call of SynapseLauncher
        expected_result = [created_matched_synapse1]

        # create a new call
        with mock.patch("kalliope.core.Lifo.LIFOBuffer.execute"):
            SynapseLauncher.start_synapse_by_list_name(["Synapse2", "Synapse3"],
                                                       brain=self.brain_test,
                                                       new_lifo=True)
            # the current singleton should be the same
            self.assertEqual(expected_result, lifo_buffer.lifo_list)

        # test to start a synapse list with the singleton lifo
        Singleton._instances = dict()
        LifoManager.clean_saved_lifo()
        lifo_buffer = LifoManager.get_singleton_lifo()
        created_matched_synapse1 = MatchedSynapse(matched_synapse=self.synapse1)
        # place a synapse in the singleton
        lifo_buffer.lifo_list = [created_matched_synapse1]
        # the current status of the singleton lifo should contain synapse launched in the next call
        created_matched_synapse2 = MatchedSynapse(matched_synapse=self.synapse2)
        created_matched_synapse3 = MatchedSynapse(matched_synapse=self.synapse3)
        expected_result = [created_matched_synapse1, [created_matched_synapse2, created_matched_synapse3]]

        with mock.patch("kalliope.core.Lifo.LIFOBuffer.execute"):
            SynapseLauncher.start_synapse_by_list_name(["Synapse2", "Synapse3"],
                                                       brain=self.brain_test)
            # the singleton should now contains the synapse that was already there and the 2 other synapses
            self.assertEqual(expected_result, lifo_buffer.lifo_list)

    def test_run_matching_synapse_from_order(self):
        # ------------------
        # test_match_synapse1
        # ------------------
        with mock.patch("kalliope.core.Lifo.LIFOBuffer.execute"):
            order_to_match = "this is the sentence"

            should_be_created_matched_synapse = MatchedSynapse(matched_synapse=self.synapse1,
                                                               user_order=order_to_match,
                                                               matched_order="this is the sentence")
            expected_result = [[should_be_created_matched_synapse]]
            SynapseLauncher.run_matching_synapse_from_order(order_to_match,
                                                            brain=self.brain_test,
                                                            settings=self.settings_test)

            lifo_buffer = LifoManager.get_singleton_lifo()
            self.assertEqual(expected_result, lifo_buffer.lifo_list)

        # -------------------------
        # test_match_synapse1_and_2
        # -------------------------
        # clean LIFO
        Singleton._instances = dict()
        LifoManager.clean_saved_lifo()
        with mock.patch("kalliope.core.Lifo.LIFOBuffer.execute"):
            order_to_match = "this is the second sentence"
            should_be_created_matched_synapse1 = MatchedSynapse(matched_synapse=self.synapse1,
                                                                user_order=order_to_match,
                                                                matched_order="this is the sentence")
            should_be_created_matched_synapse2 = MatchedSynapse(matched_synapse=self.synapse2,
                                                                user_order=order_to_match,
                                                                matched_order="this is the second sentence")

            expected_result = [[should_be_created_matched_synapse1, should_be_created_matched_synapse2]]
            SynapseLauncher.run_matching_synapse_from_order(order_to_match,
                                                            brain=self.brain_test,
                                                            settings=self.settings_test)
            lifo_buffer = LifoManager.get_singleton_lifo()
            self.assertEqual(expected_result, lifo_buffer.lifo_list)

        # -------------------------
        # test_call_hook_order_not_found
        # -------------------------
        # clean LIFO
        Singleton._instances = dict()
        LifoManager.clean_saved_lifo()
        with mock.patch("kalliope.core.HookManager.on_order_not_found") as mock_hook:
            order_to_match = "not existing sentence"

            SynapseLauncher.run_matching_synapse_from_order(order_to_match,
                                                            brain=self.brain_test,
                                                            settings=self.settings_test)
            mock_hook.assert_called_with()

        mock_hook.reset_mock()

        # -------------------------
        # test_call_hook_order_found
        # -------------------------
        # clean LIFO
        Singleton._instances = dict()
        with mock.patch("kalliope.core.Lifo.LIFOBuffer.execute"):
            with mock.patch("kalliope.core.HookManager.on_order_found") as mock_hook:
                order_to_match = "this is the second sentence"
                new_settings = Settings()
                SynapseLauncher.run_matching_synapse_from_order(order_to_match,
                                                                brain=self.brain_test,
                                                                settings=new_settings)
                mock_hook.assert_called_with()

        mock_hook.reset_mock()


if __name__ == '__main__':
    unittest.main()

    # suite = unittest.TestSuite()
    # suite.addTest(TestSynapseLauncher("test_start_synapse_by_list_name"))
    # runner = unittest.TextTestRunner()
    # runner.run(suite)
