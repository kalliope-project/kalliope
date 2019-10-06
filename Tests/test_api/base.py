import os

from flask import Flask
from flask_testing import LiveServerTestCase

from kalliope.core import LifoManager
from kalliope.core.ConfigurationManager import BrainLoader
from kalliope.core.ConfigurationManager import SettingLoader
from kalliope.core.Models import Singleton
from kalliope.core.RestAPI.FlaskAPI import FlaskAPI


class RestAPITestBase(LiveServerTestCase):

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
        if "/Tests" in current_path:
            full_path_brain_to_test = current_path + os.sep + os.pardir + os.sep + "brains/brain_test_api.yml"
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
