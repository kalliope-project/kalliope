import json
import unittest

from mock import mock

from Tests.test_api.base import RestAPITestBase
from kalliope.core.Cortex import Cortex


class TestSynapseView(RestAPITestBase):

    def test_get_all_synapses(self):
        url = self.get_server_url() + "/synapses"

        response = self.client.get(url)
        expected_content = {
            "synapses": [
                {"signals": [{"name": "order", "parameters": "test_order"}],
                 "neurons": [{"name": "say", "parameters": {"message": ["test message"]}}],
                 "name": "test", "enabled": True},
                {"signals": [{"name": "order", "parameters": "test_order_miss_configured_neuron"}],
                 "neurons": [{"name": "say", "parameters": {"not_valid_parameter": ["test message"]}}],
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

        # a lot of char to process
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

    def test_delete_synapse(self):
        # test with existing synapse
        url = self.get_server_url() + "/synapses/test"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

        # test with non existing synapse
        url = self.get_server_url() + "/synapses/test-none"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 404)
        expected_content = {
            "error": {
                "synapse name not found": "test-none"
            }
        }
        self.assertEqual(expected_content, json.loads(response.get_data().decode('utf-8')))

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
        # check that the cortex contains the last order
        self.assertEqual("test_order", Cortex.get_from_key("kalliope_last_order"))

        # test with a wrong parameter in a neuron
        data = {"order": "test_order_miss_configured_neuron"}
        result = self.client.post(url, headers=headers, data=json.dumps(data))
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
            result_file = self.flask_api.synapses_blueprint._convert_to_wav(temp_file)
            self.assertEqual(temp_file, result_file)
            mock_os_system.assert_not_called()

            # Scenario 2 : input not a wav file
            temp_file = "/tmp/kalliope/tempfile.amr"  # tempfile.NamedTemporaryFile(suffix=".wav")
            expected_result = "/tmp/kalliope/tempfile.wav"
            result_file = self.flask_api.synapses_blueprint._convert_to_wav(temp_file)
            self.assertEqual(expected_result, result_file)
            mock_os_system.assert_called_once_with("ffmpeg -loglevel panic -y -i " + temp_file + " " + expected_result)

    def test_create_synapse(self):
        url = self.get_server_url() + "/synapses"
        headers = {"Content-Type": "application/json"}

        # test with valid synapse
        data = {
            "name": "create-synapse",
            "signals": [
                {
                    "order": "I'm Batman"
                }
            ],
            "neurons": [
                {
                    "say": {
                        "message": "I know"
                    }
                }
            ]
        }

        result = self.client.post(url,
                                  headers=headers,
                                  data=json.dumps(data))

        expected_content = {
          "enabled": True,
          "name": "create-synapse",
          "neurons": [
            {
              "name": "say",
              "parameters": {
                "message": "I know"
              }
            }
          ],
          "signals": [
            {
              "name": "order",
              "parameters": "I'm Batman"
            }
          ]
        }

        self.assertEqual(result.status_code, 201)
        self.assertEqual(json.dumps(expected_content, sort_keys=True),
                         json.dumps(json.loads(result.get_data().decode('utf-8')), sort_keys=True))

        # test with non existing neuron
        data = {
            "name": "create-synapse",
            "signals": [
                {
                    "order": "I'm Batman"
                }
            ],
            "neurons": [
                {
                    "notexist": {
                        "key": "value"
                    }
                }
            ]
        }

        result = self.client.post(url,
                                  headers=headers,
                                  data=json.dumps(data))
        self.assertEqual(result.status_code, 400)

        # test with non valid synapse
        data = {
            "name": "create-synapse",
            "signals": [
                {
                    "order": "I'm Batman"
                }
            ]
        }

        result = self.client.post(url,
                                  headers=headers,
                                  data=json.dumps(data))
        self.assertEqual(result.status_code, 400)


if __name__ == '__main__':
    unittest.main()
