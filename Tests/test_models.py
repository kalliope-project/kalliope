import unittest
import ast
import mock

from kalliope.core.Models.Player import Player
from kalliope.core.Models.Signal import Signal
from kalliope.core.Models.RecognitionOptions import RecognitionOptions
from kalliope.core.Models.Tts import Tts

from kalliope.core.Models.Trigger import Trigger

from kalliope.core.Models.Stt import Stt

from kalliope.core.Models.RestAPI import RestAPI

from kalliope.core.Models.Dna import Dna

from kalliope.core import LIFOBuffer
from kalliope.core.Models.Settings import Settings

from kalliope.core.Models import Neuron, Synapse, Brain, Resources, Singleton

from kalliope.core.Models.APIResponse import APIResponse
from kalliope.core.Models.MatchedSynapse import MatchedSynapse


class TestModels(unittest.TestCase):

    def setUp(self):
        # Kill the singleton
        Singleton._instances = dict()

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

        self.all_synapse_list1 = [self.synapse1,
                                  self.synapse2,
                                  self.synapse3]

        self.all_synapse_list2 = [self.synapse2,
                                  self.synapse3]

        self.brain_test1 = Brain(synapses=self.all_synapse_list1)
        self.brain_test2 = Brain(synapses=self.all_synapse_list2)
        # this brain is the same as the first one
        self.brain_test3 = Brain(synapses=self.all_synapse_list1)

        self.settings_test = Settings()

        # clean the LiFO
        LIFOBuffer.lifo_list = list()

    def test_APIResponse(self):
        user_order = "user order"
        self.matched_synapse = MatchedSynapse(matched_synapse=self.synapse1, matched_order=user_order)

        api_response = APIResponse()
        api_response.user_order = user_order
        api_response.list_processed_matched_synapse = [self.matched_synapse]

        expected_result_serialize = {
            'status': None,
            'matched_synapses':
                [
                    {
                        'matched_order': 'user order',
                        'neuron_module_list': [],
                        'synapse_name': 'Synapse1'
                    }
                ],
                'user_order': 'user order'
        }

        self.assertDictEqual(expected_result_serialize, api_response.serialize())

    def test_Brain(self):
        # test get synapse by name
        expect_result = self.synapse1
        synapse_name = "Synapse1"
        self.assertEqual(self.brain_test1.get_synapse_by_name(synapse_name), expect_result)

        # test equals
        self.assertTrue(self.brain_test1.__eq__(self.brain_test3))

        # test not equals
        self.assertFalse(self.brain_test1.__eq__(self.brain_test2))

    def test_Dna(self):
        # create DNA object
        dna1 = Dna(name="dna1", module_type="neuron", author="kalliope",
                   kalliope_supported_version="0.4.4", tags="test")

        dna2 = Dna(name="dna2", module_type="neuron", author="community",
                   kalliope_supported_version="0.4.2", tags="other")

        # this dna is exactly the same as the first one
        dna3 = Dna(name="dna1", module_type="neuron", author="kalliope",
                   kalliope_supported_version="0.4.4", tags="test")

        expected_result_serialize = {
            'kalliope_supported_version': '0.4.4',
            'tags': 'test',
            'type': 'neuron',
            'name': 'dna1',
            'author': 'kalliope'
        }

        self.assertDictEqual(expected_result_serialize, dna1.serialize())

        self.assertTrue(dna1.__eq__(dna3))
        self.assertFalse(dna1.__eq__(dna2))

    def test_MatchedSynapse(self):
        user_order = "user order"
        matched_synapse1 = MatchedSynapse(matched_synapse=self.synapse1, matched_order=user_order)
        matched_synapse2 = MatchedSynapse(matched_synapse=self.synapse2, matched_order=user_order)
        matched_synapse3 = MatchedSynapse(matched_synapse=self.synapse1, matched_order=user_order)

        expected_result_serialize = {
            'matched_order': 'user order',
            'neuron_module_list': [],
            'synapse_name': 'Synapse1'
        }

        self.assertDictEqual(expected_result_serialize, matched_synapse1.serialize())

        self.assertTrue(matched_synapse1.__eq__(matched_synapse3))
        self.assertFalse(matched_synapse1.__eq__(matched_synapse2))

        # test neuron parameter loader is called
        with mock.patch("kalliope.core.NeuronParameterLoader.get_parameters") as mock_get_parameters:

            MatchedSynapse(matched_synapse=self.synapse1, matched_order=user_order, user_order=user_order)
            mock_get_parameters.assert_called_once_with(synapse_order=user_order,
                                                        user_order=user_order)
            mock_get_parameters.reset_mock()

    def test_Neuron(self):

        neuron1 = Neuron(name="test", parameters={"key1": "val1", "key2": "val2"})
        neuron2 = Neuron(name="test", parameters={"key3": "val3", "key4": "val4"})
        neuron3 = Neuron(name="test", parameters={"key1": "val1", "key2": "val2"})

        expected_result_serialize = {'name': 'test', 'parameters': {'key2': 'val2', 'key1': 'val1'}}

        self.assertDictEqual(expected_result_serialize, neuron1.serialize())

        self.assertTrue(neuron1.__eq__(neuron3))
        self.assertFalse(neuron1.__eq__(neuron2))

        # test password
        neuron_name = "test"
        neuron_parameters = {
            "password": "my secret",
            "parameter": "test"
        }

        neuron = Neuron()
        neuron.name = neuron_name
        neuron.parameters = neuron_parameters

        expected_result_str = "{'name': 'test', 'parameters': {'password': '*****', 'parameter': 'test'}}"

        self.assertDictEqual(ast.literal_eval(neuron.__str__()), ast.literal_eval(expected_result_str))

        neuron_name = "test"
        neuron_parameters = {
            "password_parameter": "my secret",
            "parameter": "test"
        }

        neuron = Neuron()
        neuron.name = neuron_name
        neuron.parameters = neuron_parameters

        expected_result_str = "{'name': 'test', 'parameters': {'parameter': 'test', 'password_parameter': '*****'}}"

        self.assertDictEqual(ast.literal_eval(neuron.__str__()), ast.literal_eval(expected_result_str))

    def test_Resources(self):
        resource1 = Resources(neuron_folder="/path/neuron", stt_folder="/path/stt",
                              tts_folder="/path/tts", trigger_folder="/path/trigger")

        resource2 = Resources(neuron_folder="/other_path/neuron", stt_folder="/other_path/stt",
                              tts_folder="/other_path/tts", trigger_folder="/other_path/trigger")

        resource3 = Resources(neuron_folder="/path/neuron", stt_folder="/path/stt",
                              tts_folder="/path/tts", trigger_folder="/path/trigger")

        expected_result_serialize = {
            'tts_folder': '/path/tts',
            'neuron_folder': '/path/neuron',
            'stt_folder': '/path/stt',
            'trigger_folder': '/path/trigger',
            'signal_folder': None
        }

        self.assertDictEqual(expected_result_serialize, resource1.serialize())

        self.assertTrue(resource1.__eq__(resource3))
        self.assertFalse(resource1.__eq__(resource2))

    def test_RestAPI(self):

        rest_api1 = RestAPI(password_protected=True, login="admin", password="password", active=True,
                            port=5000, allowed_cors_origin="*")

        rest_api2 = RestAPI(password_protected=False, active=False,
                            port=5000, allowed_cors_origin=None)

        rest_api3 = RestAPI(password_protected=True, login="admin", password="password", active=True,
                            port=5000, allowed_cors_origin="*")

        expected_result_serialize = {
            'password_protected': True,
            'port': 5000,
            'active': True,
            'allowed_cors_origin': '*',
            'password': 'password',
            'login': 'admin'
        }

        self.assertDictEqual(expected_result_serialize, rest_api1.serialize())

        self.assertTrue(rest_api1.__eq__(rest_api3))
        self.assertFalse(rest_api1.__eq__(rest_api2))

    def test_Settings(self):
        with mock.patch('platform.machine', return_value='pumpkins'):
            rest_api1 = RestAPI(password_protected=True,
                                login="admin",
                                password="password",
                                active=True,
                                port=5000, allowed_cors_origin="*")

            recognition_options = RecognitionOptions()

            setting1 = Settings(default_tts_name="pico2wav",
                                default_stt_name="google",
                                default_trigger_name="swoyboy",
                                default_player_name="mplayer",
                                ttss=["ttts"],
                                stts=["stts"],
                                triggers=["snowboy"],
                                players=["mplayer"],
                                rest_api=rest_api1,
                                cache_path="/tmp/kalliope",
                                resources=None,
                                variables={"key1": "val1"},
                                recognition_options=recognition_options,
                                start_options={'muted': False})
            setting1.kalliope_version = "0.4.5"

            setting2 = Settings(default_tts_name="accapela",
                                default_stt_name="bing",
                                default_trigger_name="swoyboy",
                                default_player_name="mplayer",
                                ttss=["ttts"],
                                stts=["stts"],
                                triggers=["snowboy"],
                                rest_api=rest_api1,
                                cache_path="/tmp/kalliope_tmp",
                                resources=None,
                                variables={"key1": "val1"},
                                recognition_options=recognition_options,
                                start_options={'muted': False})
            setting2.kalliope_version = "0.4.5"

            setting3 = Settings(default_tts_name="pico2wav",
                                default_stt_name="google",
                                default_trigger_name="swoyboy",
                                default_player_name="mplayer",
                                ttss=["ttts"],
                                stts=["stts"],
                                triggers=["snowboy"],
                                players=["mplayer"],
                                rest_api=rest_api1,
                                cache_path="/tmp/kalliope",
                                resources=None,
                                variables={"key1": "val1"},
                                recognition_options=recognition_options,
                                start_options={'muted': False})
            setting3.kalliope_version = "0.4.5"

            expected_result_serialize = {
                'default_tts_name': 'pico2wav',
                'hooks': None,
                'rest_api':
                    {
                        'password_protected': True,
                        'port': 5000,
                        'active': True,
                        'allowed_cors_origin': '*',
                        'password': 'password',
                        'login': 'admin'
                    },
                'default_stt_name': 'google',
                'kalliope_version': '0.4.5',
                'default_trigger_name': 'swoyboy',
                'default_player_name': 'mplayer',
                'cache_path': '/tmp/kalliope',
                'stts': ['stts'],
                'machine': 'pumpkins',
                'ttss': ['ttts'],
                'variables': {'key1': 'val1'},
                'resources': None,
                'triggers': ['snowboy'],
                'players': ['mplayer'],
                'recognition_options': {'energy_threshold': 4000, 'adjust_for_ambient_noise_second': 0},
                'start_options': {'muted': False}
            }

            self.maxDiff = None
            self.assertDictEqual(expected_result_serialize, setting1.serialize())

            self.assertTrue(setting1.__eq__(setting3))
            self.assertFalse(setting1.__eq__(setting2))

    def test_Stt(self):
        stt1 = Stt(name="stt1", parameters={"key1": "val1"})
        stt2 = Stt(name="stt2", parameters={"key2": "val2"})
        stt3 = Stt(name="stt1", parameters={"key1": "val1"})

        expected_result_serialize = {'name': 'stt1', 'parameters': {'key1': 'val1'}}

        self.assertDictEqual(expected_result_serialize, stt1.serialize())

        self.assertTrue(stt1.__eq__(stt3))
        self.assertFalse(stt1.__eq__(stt2))

    def test_Synapse(self):
        neuron1 = Neuron(name='neurone1', parameters={'var1': 'val1'})
        neuron2 = Neuron(name='neurone2', parameters={'var2': 'val2'})
        neuron3 = Neuron(name='neurone3', parameters={'var3': 'val3'})
        neuron4 = Neuron(name='neurone4', parameters={'var4': 'val4'})

        signal1 = Signal(name="order", parameters="this is the sentence")
        signal2 = Signal(name="order", parameters="this is the second sentence")

        synapse1 = Synapse(name="Synapse1", neurons=[neuron1, neuron2], signals=[signal1])
        synapse2 = Synapse(name="Synapse2", neurons=[neuron3, neuron4], signals=[signal2])
        synapse3 = Synapse(name="Synapse1", neurons=[neuron1, neuron2], signals=[signal1])

        expected_result_serialize = {
            'signals': [
                {
                    'name': 'order',
                    'parameters': 'this is the sentence'
                }
            ],
            'neurons': [
                {
                    'name': 'neurone1',
                    'parameters': {
                         'var1': 'val1'
                     }
                },
                {
                    'name': 'neurone2',
                    'parameters':
                        {
                            'var2': 'val2'
                        }
                }
            ],
            'name': 'Synapse1'
        }

        self.assertDictEqual(expected_result_serialize, synapse1.serialize())

        self.assertTrue(synapse1.__eq__(synapse3))
        self.assertFalse(synapse1.__eq__(synapse2))

    def test_Trigger(self):
        trigger1 = Trigger(name="trigger1", parameters={"key1": "val1"})
        trigger2 = Trigger(name="trigger2", parameters={"key2": "val2"})
        trigger3 = Trigger(name="trigger1", parameters={"key1": "val1"})

        expected_result_serialize = {'name': 'trigger1', 'parameters': {'key1': 'val1'}}

        self.assertDictEqual(expected_result_serialize, trigger1.serialize())

        self.assertTrue(trigger1.__eq__(trigger3))
        self.assertFalse(trigger1.__eq__(trigger2))

    def test_Player(self):
        player1 = Player(name="player1", parameters={"key1": "val1"})
        player2 = Player(name="player2", parameters={"key2": "val2"})
        player3 = Player(name="player1", parameters={"key1": "val1"})

        expected_result_serialize = {'name': 'player1', 'parameters': {'key1': 'val1'}}

        self.assertDictEqual(expected_result_serialize, player1.serialize())

        self.assertTrue(player1.__eq__(player3))
        self.assertFalse(player1.__eq__(player2))

    def test_Tts(self):
        tts1 = Tts(name="tts1", parameters={"key1": "val1"})
        tts2 = Tts(name="tts2", parameters={"key2": "val2"})
        tts3 = Tts(name="tts1", parameters={"key1": "val1"})

        expected_result_serialize = {'name': 'tts1', 'parameters': {'key1': 'val1'}}

        self.assertDictEqual(expected_result_serialize, tts1.serialize())

        self.assertTrue(tts1.__eq__(tts3))
        self.assertFalse(tts1.__eq__(tts2))


if __name__ == '__main__':
    unittest.main()

    # suite = unittest.TestSuite()
    # suite.addTest(TestLIFOBuffer("test_process_neuron_list"))
    # runner = unittest.TextTestRunner()
    # runner.run(suite)
