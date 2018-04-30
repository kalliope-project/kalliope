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
        sl = SettingLoader()
        sl.settings.rest_api.password_protected = False
        sl.settings.active = True
        sl.settings.port = 5000
        sl.settings.allowed_cors_origin = "*"
        sl.settings.default_synapse = None
        sl.settings.hooks["on_order_not_found"] = "order-not-found-synapse"

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
        url = self.get_server_url()+"/synapses"

        response = self.client.get(url)
        expected_content = {
            "synapses": [
                {"signals": [{"name": "order", "parameters": "test_order"}],
                 "neurons": [{"name": "say", "parameters": {"message": ["test message"]}}],
                 "name": "test"},
                {"signals": [{"name": "order", "parameters": "bonjour"}],
                 "neurons": [{"name": "say", "parameters": {"message": ["test message"]}}],
                 "name": "test2"},
                {"signals": [{"name": "order", "parameters": "test_order_with_parameter"}],
                 "neurons": [{"name": "say", "parameters": {"message": ["test message {{parameter1}}"]}}],
                 "name": "test4"},
                {"signals": [],
                 "neurons": [{"name": "say", "parameters": {"message": "order not found"}}],
                 "name": "order-not-found-synapse"},
                {"signals": [{"name": "order", "parameters": "test_order_3"}],
                 "neurons": [{"name": "say", "parameters": {"message": ["test message"]}}],
                 "name": "test3"}]}

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
            mock_os_system.assert_called_once_with("avconv -y -i " + temp_file + " " + expected_result)


if __name__ == '__main__':
    unittest.main()

    # suite = unittest.TestSuite()
    # suite.addTest(TestRestAPI("test_get_all_synapses"))
    # runner = unittest.TextTestRunner()
    # runner.run(suite)
