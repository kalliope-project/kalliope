import json
import unittest

import requests
import time
from flask import Flask

from core.ConfigurationManager import BrainLoader
from core.ConfigurationManager import SettingLoader
from core.RestAPI.FlaskAPI import FlaskAPI


class TestRestAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        executed once at the beginning of the test
        """
        # rest api config
        sl = SettingLoader.Instance()
        sl.settings.rest_api.password_protected = False
        sl.settings.active = True
        sl.settings.port = 5000
        # prepare a test brain
        brain_to_test = "Tests/brains/brain_test.yml"
        brain_loader = BrainLoader.Instance(file_path=brain_to_test)
        brain = brain_loader.brain

        app = Flask(__name__)
        cls.flask_api = FlaskAPI(app, port=5000, brain=brain)
        cls.flask_api.start()
        time.sleep(1)

    # @classmethod
    # def tearDownClass(cls):
    #     """
    #     executed once at the end of the test
    #     """
    #     url = "http://127.0.0.1:5000/shutdown/"
    #     requests.post(url=url)

    def setUp(self):
        self.base_url = "http://127.0.0.1:5000"

    def test_get_synapses(self):
        url = self.base_url+"/synapses/"
        result = requests.get(url=url)

        expected_content = {
            "synapses": [
                {
                    "name": "test",
                    "neurons": [
                        {
                            "say": {
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
                            "say": {
                                "message": [
                                    "test message"
                                ]
                            }
                        }
                    ],
                    "signals": [
                        {
                            "order": "test_order_2"
                        }
                    ]
                },
                {
                    "includes": [
                        "included_brain_test.yml"
                    ]
                },
                {
                    "name": "test3",
                    "neurons": [
                        {
                            "say": {
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

        self.assertEqual(expected_content, json.loads(result.content))

    def test_get_one_synapse(self):
        url = self.base_url+"/synapses/test"
        result = requests.get(url=url)

        expected_content = {
            "synapses": {
                "name": "test",
                "neurons": [
                    {
                        "say": {
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

        self.assertEqual(expected_content, json.loads(result.content))

    def test_get_synapse_not_found(self):
        url = self.base_url + "/synapses/test-none"
        result = requests.get(url=url)

        expected_content = {
            "error": {
                "synapse name not found": "test-none"
            }
        }

        self.assertEqual(expected_content, json.loads(result.content))
        self.assertEqual(result.status_code, 404)

    def test_run_synapse_by_name(self):
        url = self.base_url + "/synapses/test"
        result = requests.post(url=url)

        expected_content = {
            "synapses": {
                "name": "test",
                "neurons": [
                    {
                        "say": {
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

        self.assertEqual(expected_content, json.loads(result.content))
        self.assertEqual(result.status_code, 201)

    def test_post_synapse_not_found(self):
        url = self.base_url + "/synapses/test-none"
        result = requests.post(url=url)

        expected_content = {
            "error": {
                "synapse name not found": "test-none"
            }
        }

        self.assertEqual(expected_content, json.loads(result.content))
        self.assertEqual(result.status_code, 404)

    def test_run_synapse_with_order(self):
        url = self.base_url + "/order/"
        headers = {"Content-Type": "application/json"}
        data = {"order": "test_order"}
        result = requests.post(url=url, headers=headers, json=data)

        expected_content = {
            "synapses": [
                {
                    "name": "test",
                    "neurons": [
                        {
                            "name": "say",
                            "parameters": "{'message': ['test message']}"
                        }
                    ],
                    "signals": [
                        {
                            "order": "test_order"
                        }
                    ]
                }
            ]
        }

        self.assertEqual(expected_content, json.loads(result.content))
        self.assertEqual(result.status_code, 201)

    def test_post_synapse_by_order_not_found(self):
        url = self.base_url + "/order/"
        data = {"order": "non existing order"}
        headers = {"Content-Type": "application/json"}
        result = requests.post(url=url, headers=headers, json=data)

        expected_content = {'error': {'error': "The given order doesn't match any synapses"}}

        self.assertEqual(expected_content, json.loads(result.content))
        self.assertEqual(result.status_code, 400)

if __name__ == '__main__':
    unittest.main()
