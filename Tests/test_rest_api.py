import json
import os
import unittest

from flask import Flask
from flask_testing import LiveServerTestCase

from kalliope.core import LIFOBuffer
from kalliope.core.Models import Singleton
from kalliope._version import version_str
from kalliope.core.ConfigurationManager import BrainLoader
from kalliope.core.ConfigurationManager import SettingLoader
from kalliope.core.RestAPI.FlaskAPI import FlaskAPI


class TestRestAPI(LiveServerTestCase):

    def tearDown(self):
        Singleton._instances = {}
        # clean the lifo
        LIFOBuffer.lifo_list = list()

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
        self.assertEqual(json.dumps(expected_content), json.dumps(json.loads(response.get_data())))

    def test_get_all_synapses(self):
        url = self.get_server_url()+"/synapses"

        response = self.client.get(url)
        expected_content = {
            "synapses": [
                {
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
                            "order": "test_order"
                        }
                    ]
                },
                {
                    "name": "test2",
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
                            "order": "bonjour"
                        }
                    ]
                },
                {
                    "name": "test3",
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
                            "order": "test_order_3"
                        }
                    ]
                }
            ]
        }
        # a lot of char ti process
        self.maxDiff = None
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.dumps(expected_content), json.dumps(json.loads(response.get_data())))

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
                        "order": "test_order"
                    }
                ]
            }
        }
        self.assertEqual(json.dumps(expected_content), json.dumps(json.loads(response.get_data())))

    def test_get_synapse_not_found(self):
        url = self.get_server_url() + "/synapses/test-none"
        result = self.client.get(url)

        expected_content = {
            "error": {
                "synapse name not found": "test-none"
            }
        }

        self.assertEqual(expected_content, json.loads(result.get_data()))
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
        self.assertEqual(json.dumps(expected_content), json.dumps(json.loads(result.get_data())))
        self.assertEqual(result.status_code, 201)

    def test_post_synapse_not_found(self):
        url = self.get_server_url() + "/synapses/start/id/test-none"
        result = self.client.post(url)

        expected_content = {
            "error": {
                "synapse name not found": "test-none"
            }
        }

        self.assertEqual(json.dumps(expected_content), json.dumps(json.loads(result.get_data())))
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
        self.assertEqual(json.dumps(expected_content), json.dumps(json.loads(result.get_data())))
        self.assertEqual(result.status_code, 201)

    def test_post_synapse_by_order_not_found(self):
        url = self.get_server_url() + "/synapses/start/order"
        data = {"order": "non existing order"}
        headers = {"Content-Type": "application/json"}
        result = self.client.post(url,
                                  headers=headers,
                                  data=json.dumps(data))

        expected_content = {'status': None, 'matched_synapses': [], 'user_order': u'non existing order'}

        self.assertEqual(json.dumps(expected_content), json.dumps(json.loads(result.get_data())))
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

if __name__ == '__main__':
    unittest.main()

    # suite = unittest.TestSuite()
    # suite.addTest(TestRestAPI("test_post_synapse_by_order_not_found"))
    # runner = unittest.TextTestRunner()
    # runner.run(suite)
