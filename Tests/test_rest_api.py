import os
import unittest

from flask import Flask
from flask_testing import LiveServerTestCase

from kalliope.core.Models import Singleton

from kalliope.core.ConfigurationManager import BrainLoader
from kalliope.core.ConfigurationManager import SettingLoader
from kalliope.core.RestAPI.FlaskAPI import FlaskAPI


class TestRestAPI(LiveServerTestCase):

    def create_app(self):
        """
        executed once at the beginning of the test
        """
        # be sure that the singleton haven't been loaded before
        Singleton._instances = {}
        current_path = os.getcwd()
        full_path_brain_to_test = current_path + os.sep + "Tests/brains/brain_test.yml"
        print full_path_brain_to_test

        # rest api config
        sl = SettingLoader()
        sl.settings.rest_api.password_protected = False
        sl.settings.active = True
        sl.settings.port = 5000

        # prepare a test brain
        brain_to_test = full_path_brain_to_test
        brain_loader = BrainLoader(file_path=brain_to_test)
        brain = brain_loader.brain

        self.app = Flask(__name__)
        self.flask_api = FlaskAPI(self.app, port=5000, brain=brain)
        self.flask_api.app.config['TESTING'] = True
        return self.flask_api.app

    # TODO all following test passes with 'python -m unittest Tests.TestRestAPI' but not with discover
    # def test_get_all_synapses(self):
    #     url = "http://127.0.0.1:5000/synapses"
    #
    #     result = requests.get(url=url)
    #     expected_content = {
    #         "synapses": [
    #             {
    #                 "name": "test",
    #                 "neurons": [
    #                     {
    #                         "say": {
    #                             "message": [
    #                                 "test message"
    #                             ]
    #                         }
    #                     }
    #                 ],
    #                 "signals": [
    #                     {
    #                         "order": "test_order"
    #                     }
    #                 ]
    #             },
    #             {
    #                 "name": "test2",
    #                 "neurons": [
    #                     {
    #                         "say": {
    #                             "message": [
    #                                 "test message"
    #                             ]
    #                         }
    #                     }
    #                 ],
    #                 "signals": [
    #                     {
    #                         "order": "test_order_2"
    #                     }
    #                 ]
    #             },
    #             {
    #                 "includes": [
    #                     "included_brain_test.yml"
    #                 ]
    #             },
    #             {
    #                 "name": "test3",
    #                 "neurons": [
    #                     {
    #                         "say": {
    #                             "message": [
    #                                 "test message"
    #                             ]
    #                         }
    #                     }
    #                 ],
    #                 "signals": [
    #                     {
    #                         "order": "test_order_3"
    #                     }
    #                 ]
    #             }
    #         ]
    #     }
    #
    #     self.assertEqual(result.status_code, 200)
    #     self.assertEqual(expected_content, json.loads(result.content))
    #
    # def test_get_one_synapse(self):
    #     url = "http://127.0.0.1:5000/synapses/test"
    #     result = requests.get(url=url)
    #
    #     expected_content = {
    #         "synapses": {
    #             "name": "test",
    #             "neurons": [
    #                 {
    #                     "say": {
    #                         "message": [
    #                             "test message"
    #                         ]
    #                     }
    #                 }
    #             ],
    #             "signals": [
    #                 {
    #                     "order": "test_order"
    #                 }
    #             ]
    #         }
    #     }
    #
    #     self.assertEqual(expected_content, json.loads(result.content))
    #
    # def test_get_synapse_not_found(self):
    #     url = "http://127.0.0.1:5000/synapses/test-none"
    #     result = requests.get(url=url)
    #
    #     expected_content = {
    #         "error": {
    #             "synapse name not found": "test-none"
    #         }
    #     }
    #
    #     self.assertEqual(expected_content, json.loads(result.content))
    #     self.assertEqual(result.status_code, 404)
    #
    # def test_run_synapse_by_name(self):
    #     url = "http://127.0.0.1:5000/synapses/test"
    #     result = requests.post(url=url)
    #
    #     expected_content = {
    #         "synapses": {
    #             "name": "test",
    #             "neurons": [
    #                 {
    #                     "say": {
    #                         "message": [
    #                             "test message"
    #                         ]
    #                     }
    #                 }
    #             ],
    #             "signals": [
    #                 {
    #                     "order": "test_order"
    #                 }
    #             ]
    #         }
    #     }
    #
    #     self.assertEqual(expected_content, json.loads(result.content))
    #     self.assertEqual(result.status_code, 201)
    #
    # def test_post_synapse_not_found(self):
    #     url = "http://127.0.0.1:5000/synapses/test-none"
    #     result = requests.post(url=url)
    #
    #     expected_content = {
    #         "error": {
    #             "synapse name not found": "test-none"
    #         }
    #     }
    #
    #     self.assertEqual(expected_content, json.loads(result.content))
    #     self.assertEqual(result.status_code, 404)
    #
    # def test_run_synapse_with_order(self):
    #     url = "http://127.0.0.1:5000/order/"
    #     headers = {"Content-Type": "application/json"}
    #     data = {"order": "test_order"}
    #     result = requests.post(url=url, headers=headers, json=data)
    #
    #     expected_content = {
    #         "synapses": [
    #             {
    #                 "name": "test",
    #                 "neurons": [
    #                     {
    #                         "name": "say",
    #                         "parameters": "{'message': ['test message']}"
    #                     }
    #                 ],
    #                 "signals": [
    #                     {
    #                         "order": "test_order"
    #                     }
    #                 ]
    #             }
    #         ]
    #     }
    #
    #     self.assertEqual(expected_content, json.loads(result.content))
    #     self.assertEqual(result.status_code, 201)
    #
    # def test_post_synapse_by_order_not_found(self):
    #     url = "http://127.0.0.1:5000/order/"
    #     data = {"order": "non existing order"}
    #     headers = {"Content-Type": "application/json"}
    #     result = requests.post(url=url, headers=headers, json=data)
    #
    #     expected_content = {'error': {'error': "The given order doesn't match any synapses"}}
    #
    #     self.assertEqual(expected_content, json.loads(result.content))
    #     self.assertEqual(result.status_code, 400)

if __name__ == '__main__':
    unittest.main()
