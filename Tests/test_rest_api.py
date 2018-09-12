import json
import os
import unittest

from flask import Flask
from flask_testing import LiveServerTestCase
from mock import mock

from kalliope._version import version_str
from kalliope.core import LifoManager
from kalliope.core.ConfigurationManager import BrainLoader
from kalliope.core.ConfigurationManager import SettingLoader
from kalliope.core.Models import Singleton
from kalliope.core.RestAPI.FlaskAPI import FlaskAPI


class TestRestAPI(LiveServerTestCase):

    def tearDown(self):
        Singleton._instances = {}
        # clean the lifo
        LifoManager.clean_saved_lifo()

    def create_app(self):
        """
        executed once at the beginning of the test
        """
        # be sure that the singleton haven't been loaded before
        Singleton._instances = {}
        current_path = os.getcwd()
        if "/Tests" in os.getcwd():
            full_path_brain_to_test = current_path + os.sep + "brains/brain_test_api.yml"
            self.audio_file = "files/bonjour.wav"
        else:
            full_path_brain_to_test = current_path + os.sep + "Tests/brains/brain_test_api.yml"
            self.audio_file = "Tests/files/bonjour.wav"

        # rest api config
        self.sl = SettingLoader()
        self.settings = self.sl.settings
        self.settings.rest_api.password_protected = False
        self.settings.active = True
        self.settings.port = 5000
        self.settings.allowed_cors_origin = "*"
        self.settings.default_synapse = None
        self.settings.hooks["on_order_not_found"] = "order-not-found-synapse"

        # prepare a test brain
        brain_to_test = full_path_brain_to_test
        brain_loader = BrainLoader(file_path=brain_to_test)
        brain = brain_loader.brain

        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.flask_api = FlaskAPI(self.app, port=5000, brain=brain)
        self.client = self.app.test_client()
        return self.flask_api.app

    def test_server_is_up_and_running(self):
        # response = urllib2.urlopen(self.get_server_url())
        response = self.client.get(self.get_server_url())
        self.assertEqual(response.status_code, 200)

    def test_get_main_page(self):
        url = self.get_server_url() + "/"
        response = self.client.get(url)
        expected_content = {
            "Kalliope version": "%s" % version_str
        }
        self.assertEqual(json.dumps(expected_content, sort_keys=True),
                         json.dumps(json.loads(response.get_data().decode('utf-8')), sort_keys=True))

    def test_get_all_synapses(self):
        url = self.get_server_url() + "/synapses"

        response = self.client.get(url)
        expected_content = {
            "synapses": [
                {"signals": [{"name": "order", "parameters": "test_order"}],
                 "neurons": [{"name": "say", "parameters": {"message": ["test message"]}}],
                 "name": "test", "enabled": True},
                {"signals": [{"name": "order", "parameters": "bonjour"}],
                 "neurons": [{"name": "say", "parameters": {"message": ["test message"]}}],
                 "name": "test2", "enabled": True},
                {"signals": [{"name": "order", "parameters": "test_order_with_parameter"}],
                 "neurons": [{"name": "say", "parameters": {"message": ["test message {{parameter1}}"]}}],
                 "name": "test4", "enabled": True},
                {"signals": [],
                 "neurons": [{"name": "say", "parameters": {"message": "order not found"}}],
                 "name": "order-not-found-synapse", "enabled": True},
                {"signals": [{"name": "order", "parameters": "test_order_3"}],
                 "neurons": [{"name": "say", "parameters": {"message": ["test message"]}}],
                 "name": "test3", "enabled": True}]}

        # a lot of char ti process
        self.maxDiff = None
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.dumps(expected_content, sort_keys=True),
                         json.dumps(json.loads(response.get_data().decode('utf-8')), sort_keys=True))

    def test_get_one_synapse(self):
        url = self.get_server_url() + "/synapses/test"
        response = self.client.get(url)

        expected_content = {
            "synapses": {
                "name": "test",
                'enabled': True,
                "neurons": [
                    {
                        "name": "say",
                        "parameters": {
                            "message": [
                                "test message"
                            ]
                        }
                    }
                ],
                "signals": [
                    {
                        "name": "order",
                        "parameters": "test_order"
                    }
                ]
            }
        }
        self.assertEqual(json.dumps(expected_content, sort_keys=True),
                         json.dumps(json.loads(response.get_data().decode('utf-8')), sort_keys=True))

    def test_get_synapse_not_found(self):
        url = self.get_server_url() + "/synapses/test-none"
        result = self.client.get(url)

        expected_content = {
            "error": {
                "synapse name not found": "test-none"
            }
        }

        self.assertEqual(expected_content, json.loads(result.get_data().decode('utf-8')))
        self.assertEqual(result.status_code, 404)

    def test_run_synapse_by_name(self):
        url = self.get_server_url() + "/synapses/start/id/test"
        result = self.client.post(url)

        expected_content = {'status': 'complete',
                            'matched_synapses':
                                [{'matched_order': None,
                                  'neuron_module_list':
                                      [{'generated_message': 'test message', 'neuron_name': 'Say'}],
                                  'synapse_name': 'test'}],
                            'user_order': None
                            }
        self.assertEqual(json.dumps(expected_content, sort_keys=True),
                         json.dumps(json.loads(result.get_data().decode('utf-8')), sort_keys=True))
        self.assertEqual(result.status_code, 201)

        # run a synapse by its name with parameter
        url = self.get_server_url() + "/synapses/start/id/test4"
        headers = {"Content-Type": "application/json"}
        data = {"parameters": {"parameter1": "replaced_value"}}
        result = self.client.post(url, headers=headers, data=json.dumps(data))

        expected_content = {
            "matched_synapses": [
                {
                    "matched_order": None,
                    "neuron_module_list": [
                        {
                            "generated_message": "test message replaced_value",
                            "neuron_name": "Say"
                        }
                    ],
                    "synapse_name": "test4"
                }
            ],
            "status": "complete",
            "user_order": None
        }

        self.assertEqual(json.dumps(expected_content, sort_keys=True),
                         json.dumps(json.loads(result.get_data().decode('utf-8')), sort_keys=True))
        self.assertEqual(result.status_code, 201)

    def test_post_synapse_not_found(self):
        url = self.get_server_url() + "/synapses/start/id/test-none"
        result = self.client.post(url)

        expected_content = {
            "error": {
                "synapse name not found": "test-none"
            }
        }

        self.assertEqual(json.dumps(expected_content, sort_keys=True),
                         json.dumps(json.loads(result.get_data().decode('utf-8')), sort_keys=True))
        self.assertEqual(result.status_code, 404)

    def test_run_synapse_with_order(self):
        url = self.get_server_url() + "/synapses/start/order"
        headers = {"Content-Type": "application/json"}
        data = {"order": "test_order"}
        result = self.client.post(url, headers=headers, data=json.dumps(data))

        expected_content = {'status': 'complete',
                            'matched_synapses':
                                [
                                    {
                                        'matched_order': "test_order",
                                        'neuron_module_list':
                                            [
                                                {
                                                    'generated_message': 'test message', 'neuron_name': 'Say'
                                                }
                                            ],
                                        'synapse_name': 'test'
                                    }
                                ],
                            'user_order': "test_order"
                            }
        self.assertEqual(json.dumps(expected_content, sort_keys=True),
                         json.dumps(json.loads(result.get_data().decode('utf-8')), sort_keys=True))
        self.assertEqual(result.status_code, 201)

    def test_post_synapse_by_order_not_found(self):
        url = self.get_server_url() + "/synapses/start/order"
        data = {"order": "non existing order"}
        headers = {"Content-Type": "application/json"}
        result = self.client.post(url,
                                  headers=headers,
                                  data=json.dumps(data))

        expected_content = {"matched_synapses": [{"matched_order": None,
                                                  "neuron_module_list": [
                                                      {"generated_message": "order not found",
                                                       "neuron_name": "Say"}
                                                  ],
                                                  "synapse_name": "order-not-found-synapse"}],
                            "status": "complete",
                            "user_order": None}

        self.assertEqual(json.dumps(expected_content, sort_keys=True),
                         json.dumps(json.loads(result.get_data().decode('utf-8')), sort_keys=True))
        self.assertEqual(result.status_code, 201)

        # TODO this doesn't work on travis but works locally with python -m unittest discover
        # def test_post_synapse_by_audio(self):
        #     url = self.get_server_url() + "/synapses/start/audio"
        #     with open(os.path.join(self.audio_file), 'rb') as fp:
        #         file = FileStorage(fp)
        #         data = {
        #             'file': file
        #         }
        #         result = self.client.post(url, data=data, content_type='multipart/form-data')
        #
        #         expected_content = {
        #             "synapses": [
        #                 {
        #                     "name": "test2",
        #                     "neurons": [
        #                         {
        #                             "name": "say",
        #                             "parameters": {
        #                                 "message": [
        #                                     "test message"
        #                                 ]
        #                             }
        #                         }
        #                     ],
        #                     "signals": [
        #                         {
        #                             "order": "bonjour"
        #                         }
        #                     ]
        #                 }
        #             ]
        #         }
        #
        #         self.assertEqual(json.dumps(expected_content), json.dumps(json.loads(result.get_data())))
        #         self.assertEqual(result.status_code, 201)

    def test_convert_to_wav(self):
        """
        Test the api function to convert incoming sound file to wave.
        """

        with mock.patch("os.system") as mock_os_system:
            # Scenario 1 : input wav file
            temp_file = "/tmp/kalliope/tempfile.wav"  # tempfile.NamedTemporaryFile(suffix=".wav")
            result_file = FlaskAPI._convert_to_wav(temp_file)
            self.assertEqual(temp_file, result_file)
            mock_os_system.assert_not_called()

            # Scenario 2 : input not a wav file
            temp_file = "/tmp/kalliope/tempfile.amr"  # tempfile.NamedTemporaryFile(suffix=".wav")
            expected_result = "/tmp/kalliope/tempfile.wav"
            result_file = FlaskAPI._convert_to_wav(temp_file)
            self.assertEqual(expected_result, result_file)
            mock_os_system.assert_called_once_with("ffmpeg -loglevel panic -y -i " + temp_file + " " + expected_result)

    def test_get_mute(self):
        """
        Test for api get mute.
        """
        url = self.get_server_url() + "/settings/mute"
        headers = {"Content-Type": "application/json"}

        self.settings.options.mute = False
        result = self.client.get(url, headers=headers)

        expected_content = {
            "mute": False
        }

        self.assertEqual(json.dumps(expected_content, sort_keys=True),
                         json.dumps(json.loads(result.get_data().decode('utf-8')), sort_keys=True))
        self.assertEqual(result.status_code, 200)

    def test_set_mute(self):
        """
        Test for api set mute.
        """
        url = self.get_server_url() + "/settings/mute"
        data = {"mute": "True"}
        headers = {"Content-Type": "application/json"}

        self.settings.options.mute = False
        result = self.client.post(url,
                                  headers=headers,
                                  data=json.dumps(data))

        expected_content = {
            "mute": True
        }

        self.assertEqual(json.dumps(expected_content, sort_keys=True),
                         json.dumps(json.loads(result.get_data().decode('utf-8')), sort_keys=True))
        self.assertEqual(result.status_code, 200)

    def test_get_deaf(self):
        """
        Test for api get deaf.
        """
        url = self.get_server_url() + "/settings/deaf"
        headers = {"Content-Type": "application/json"}

        self.settings.options.deaf = False
        result = self.client.get(url, headers=headers)

        expected_content = {
            "deaf": False
        }

        self.assertEqual(json.dumps(expected_content, sort_keys=True),
                         json.dumps(json.loads(result.get_data().decode('utf-8')), sort_keys=True))
        self.assertEqual(result.status_code, 200)

    def test_set_deaf(self):
        """
        Test for api set deaf.
        """
        url = self.get_server_url() + "/settings/deaf"
        data = {"deaf": "True"}
        headers = {"Content-Type": "application/json"}

        self.settings.options.deaf = False
        with mock.patch("kalliope.core.SignalLauncher.SignalLauncher.get_order_instance") as mock_order:
            result = self.client.post(url,
                                      headers=headers,
                                      data=json.dumps(data))

            expected_content = {
                "deaf": True
            }

            mock_order.assert_called_once()
            self.assertEqual(json.dumps(expected_content, sort_keys=True),
                             json.dumps(json.loads(result.get_data().decode('utf-8')), sort_keys=True))
            self.assertEqual(result.status_code, 200)

    def test_get_energy_threshold(self):
        """
        Test for api get energy threshold.
        """
        url = self.get_server_url() + "/settings/energy_threshold"
        headers = {"Content-Type": "application/json"}
        self.settings.options.energy_threshold = 3000
        result = self.client.get(url, headers=headers)

        expected_content = {
            "energy_threshold": 3000
        }

        self.assertEqual(json.dumps(expected_content, sort_keys=True),
                         json.dumps(json.loads(result.get_data().decode('utf-8')), sort_keys=True))
        self.assertEqual(result.status_code, 200)

    def test_set_energy_threshold(self):
        """
        Test for api set energy_threshold.
        """
        url = self.get_server_url() + "/settings/energy_threshold"
        data = {"energy_threshold": "6000"}
        headers = {"Content-Type": "application/json"}

        self.settings.energy_threshold = 4000
        result = self.client.post(url,
                                  headers=headers,
                                  data=json.dumps(data))

        expected_content = {
            "energy_threshold": "6000"
        }

        self.assertEqual(json.dumps(expected_content, sort_keys=True),
                         json.dumps(json.loads(result.get_data().decode('utf-8')), sort_keys=True))
        self.assertEqual(result.status_code, 200)

    def test_get_ambient_noise_second(self):
        """
        Test for api get adjust ambient noise second.
        """
        url = self.get_server_url() + "/settings/ambient_noise_second"
        headers = {"Content-Type": "application/json"}
        self.settings.options.adjust_for_ambient_noise_second= 30
        result = self.client.get(url, headers=headers)

        expected_content = {
            "ambient_noise_second": 30
        }

        self.assertEqual(json.dumps(expected_content, sort_keys=True),
                         json.dumps(json.loads(result.get_data().decode('utf-8')), sort_keys=True))
        self.assertEqual(result.status_code, 200)

    def test_set_ambient_noise_second(self):
        """
        Test for api set ambient_noise_second.
        """
        url = self.get_server_url() + "/settings/ambient_noise_second"
        data = {"ambient_noise_second": "60"}
        headers = {"Content-Type": "application/json"}

        self.settings.energy_threshold = 40
        result = self.client.post(url,
                                  headers=headers,
                                  data=json.dumps(data))

        expected_content = {
            "ambient_noise_second": "60"
        }

        self.assertEqual(json.dumps(expected_content, sort_keys=True),
                         json.dumps(json.loads(result.get_data().decode('utf-8')), sort_keys=True))
        self.assertEqual(result.status_code, 200)

    def test_get_default_tts(self):
        """
        Test for api get default tts name.
        """
        url = self.get_server_url() + "/settings/default_tts"
        headers = {"Content-Type": "application/json"}
        self.settings.default_tts_name= "test"
        result = self.client.get(url, headers=headers)

        expected_content = {
            "default_tts": "test"
        }

        self.assertEqual(json.dumps(expected_content, sort_keys=True),
                         json.dumps(json.loads(result.get_data().decode('utf-8')), sort_keys=True))
        self.assertEqual(result.status_code, 200)

    def test_set_default_tts(self):
        """
        Test for api set default_tts.
        """
        url = self.get_server_url() + "/settings/default_tts"
        data = {"default_tts": "pico2wave"}
        headers = {"Content-Type": "application/json"}

        self.settings.default_tts_name = "test"
        result = self.client.post(url,
                                  headers=headers,
                                  data=json.dumps(data))

        expected_content = {
            "default_tts": "pico2wave"
        }

        self.assertEqual(json.dumps(expected_content, sort_keys=True),
                         json.dumps(json.loads(result.get_data().decode('utf-8')), sort_keys=True))
        self.assertEqual(result.status_code, 200)

    def test_get_default_stt(self):
        """
        Test for api get default stt name.
        """
        url = self.get_server_url() + "/settings/default_stt"
        headers = {"Content-Type": "application/json"}
        self.settings.default_stt_name= "test"
        result = self.client.get(url, headers=headers)

        expected_content = {
            "default_stt": "test"
        }

        self.assertEqual(json.dumps(expected_content, sort_keys=True),
                         json.dumps(json.loads(result.get_data().decode('utf-8')), sort_keys=True))
        self.assertEqual(result.status_code, 200)

    def test_set_default_stt(self):
        """
        Test for api set default_stt.
        """
        url = self.get_server_url() + "/settings/default_stt"
        data = {"default_stt": "google"}
        headers = {"Content-Type": "application/json"}

        self.settings.default_stt_name = "test"
        result = self.client.post(url,
                                  headers=headers,
                                  data=json.dumps(data))

        expected_content = {
            "default_stt": "google"
        }

        self.assertEqual(json.dumps(expected_content, sort_keys=True),
                         json.dumps(json.loads(result.get_data().decode('utf-8')), sort_keys=True))
        self.assertEqual(result.status_code, 200)

    def test_get_default_player(self):
        """
        Test for api get default player.
        """
        url = self.get_server_url() + "/settings/default_player"
        headers = {"Content-Type": "application/json"}
        self.settings.default_player_name= "test"
        result = self.client.get(url, headers=headers)

        expected_content = {
            "default_player": "test"
        }

        self.assertEqual(json.dumps(expected_content, sort_keys=True),
                         json.dumps(json.loads(result.get_data().decode('utf-8')), sort_keys=True))
        self.assertEqual(result.status_code, 200)

    def test_set_default_player(self):
        """
        Test for api set default_player.
        """
        url = self.get_server_url() + "/settings/default_player"
        data = {"default_player": "mplayer"}
        headers = {"Content-Type": "application/json"}

        self.settings.default_player_name = "test"
        result = self.client.post(url,
                                  headers=headers,
                                  data=json.dumps(data))

        expected_content = {
            "default_player": "mplayer"
        }

        self.assertEqual(json.dumps(expected_content, sort_keys=True),
                         json.dumps(json.loads(result.get_data().decode('utf-8')), sort_keys=True))
        self.assertEqual(result.status_code, 200)

    def test_get_default_trigger(self):
        """
        Test for api get default trigger.
        """
        url = self.get_server_url() + "/settings/default_trigger"
        headers = {"Content-Type": "application/json"}
        self.settings.default_trigger_name= "test"
        result = self.client.get(url, headers=headers)

        expected_content = {
            "default_trigger": "test"
        }

        self.assertEqual(json.dumps(expected_content, sort_keys=True),
                         json.dumps(json.loads(result.get_data().decode('utf-8')), sort_keys=True))
        self.assertEqual(result.status_code, 200)

    def test_set_default_trigger(self):
        """
        Test for api set default_trigger.
        """
        url = self.get_server_url() + "/settings/default_trigger"
        data = {"default_trigger": "snowboy"}
        headers = {"Content-Type": "application/json"}

        self.settings.default_trigger_name = "test"
        result = self.client.post(url,
                                  headers=headers,
                                  data=json.dumps(data))

        expected_content = {
            "default_trigger": "snowboy"
        }

        self.assertEqual(json.dumps(expected_content, sort_keys=True),
                         json.dumps(json.loads(result.get_data().decode('utf-8')), sort_keys=True))
        self.assertEqual(result.status_code, 200)

    def test_get_hooks(self):
        """
        Test for api get hooks.
        """
        url = self.get_server_url() + "/settings/hooks"
        headers = {"Content-Type": "application/json"}
        self.settings.hooks = {
            "on_start": "on-start-synapse",
            "on_waiting_for_trigger":{},
            "on_triggered": "on-triggered-synapse",
            "on_start_listening":{},
            "on_stop_listening":{},
            "on_order_found":{},
            "on_order_not_found": "order-not-found-synapse",
            "on_processed_synapses":{},
            "on_deaf":{},
            "on_undeaf":{},
            "on_start_speaking":{},
            "on_stop_speaking":{},
            "on_stt_error":{}
        }
        result = self.client.get(url, headers=headers)

        expected_content = {
            "hooks": {
                "on_start": "on-start-synapse",
                "on_waiting_for_trigger":{},
                "on_triggered": "on-triggered-synapse",
                "on_start_listening":{},
                "on_stop_listening":{},
                "on_order_found":{},
                "on_order_not_found": "order-not-found-synapse",
                "on_processed_synapses":{},
                "on_deaf":{},
                "on_undeaf":{},
                "on_start_speaking":{},
                "on_stop_speaking":{},
                "on_stt_error":{}
            }
        }

        self.assertEqual(json.dumps(expected_content, sort_keys=True),
                         json.dumps(json.loads(result.get_data().decode('utf-8')), sort_keys=True))
        self.assertEqual(result.status_code, 200)

    def test_set_hooks(self):
        """
        Test for api set hooks.
        """
        url = self.get_server_url() + "/settings/hooks"
        data = {"on_waiting_for_trigger": "synapse"}
        headers = {"Content-Type": "application/json"}

        self.settings.hooks = {
            "on_start": "on-start-synapse",
            "on_waiting_for_trigger":{},
            "on_triggered": "on-triggered-synapse",
            "on_start_listening":{},
            "on_stop_listening":{},
            "on_order_found":{},
            "on_order_not_found": "order-not-found-synapse",
            "on_processed_synapses":{},
            "on_deaf":{},
            "on_undeaf":{},
            "on_start_speaking":{},
            "on_stop_speaking":{},
            "on_stt_error":{}
        }

        result = self.client.post(url,
                                  headers=headers,
                                  data=json.dumps(data))

        expected_content = {
            "hooks": {
                "on_start": "on-start-synapse",
                "on_waiting_for_trigger": "synapse",
                "on_triggered": "on-triggered-synapse",
                "on_start_listening":{},
                "on_stop_listening":{},
                "on_order_found":{},
                "on_order_not_found": "order-not-found-synapse",
                "on_processed_synapses":{},
                "on_deaf":{},
                "on_undeaf":{},
                "on_start_speaking":{},
                "on_stop_speaking":{},
                "on_stt_error":{}
            }
        }

        self.assertEqual(json.dumps(expected_content, sort_keys=True),
                         json.dumps(json.loads(result.get_data().decode('utf-8')), sort_keys=True))
        self.assertEqual(result.status_code, 200)

    def test_get_variables(self):
        """
        Test for api get variables.
        """
        url = self.get_server_url() + "/settings/variables"
        headers = {"Content-Type": "application/json"}
        self.settings.variables = {
            "test": "tust",
            "tost":"tist"
        }
        result = self.client.get(url, headers=headers)

        expected_content = {
            "variables": {
                "test": "tust",
                "tost": "tist"
            }
        }

        self.assertEqual(json.dumps(expected_content, sort_keys=True),
                         json.dumps(json.loads(result.get_data().decode('utf-8')), sort_keys=True))
        self.assertEqual(result.status_code, 200)

    def test_set_variables(self):
        """
        Test for api set variables.
        """
        url = self.get_server_url() + "/settings/variables"
        data = {"toto": "titi"}
        headers = {"Content-Type": "application/json"}

        self.settings.variables = {
            "tt": "aa",
            "uu":"ii"
        }

        result = self.client.post(url,
                                  headers=headers,
                                  data=json.dumps(data))

        expected_content = {
            "variables": {
                "tt": "aa",
                "uu":"ii",
                "toto": "titi"
            }
        }

        self.assertEqual(json.dumps(expected_content, sort_keys=True),
                         json.dumps(json.loads(result.get_data().decode('utf-8')), sort_keys=True))
        self.assertEqual(result.status_code, 200)


if __name__ == '__main__':
    unittest.main()
