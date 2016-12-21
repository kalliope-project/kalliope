import os
import inspect
import platform
import shutil
import unittest

from kalliope.core.ConfigurationManager import SettingLoader
from kalliope.core.Models import Singleton
from kalliope.core.Models import Resources
from kalliope.core.Models.RestAPI import RestAPI
from kalliope.core.Models.Settings import Settings
from kalliope.core.Models.Stt import Stt
from kalliope.core.Models.Trigger import Trigger
from kalliope.core.Models.Tts import Tts


class TestSettingLoader(unittest.TestCase):

    def setUp(self):
        # get current script directory path. We are in /an/unknown/path/kalliope/core/Tests
        cur_script_directory = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        # get parent dir. Now we are in /an/unknown/path/kalliope
        root_dir = os.path.normpath(cur_script_directory + os.sep + os.pardir)

        self.settings_file_to_test = root_dir + os.sep + "Tests/settings/settings_test.yml"

        self.settings_dict = {
            'rest_api':
                {'active': True,
                 'login': 'admin',
                 'password': 'secret',
                 'password_protected': True,
                 'port': 5000},
            'default_trigger': 'snowboy',
            'triggers': [{'snowboy': {'pmdl_file': 'trigger/snowboy/resources/kalliope-FR-6samples.pmdl'}}],
            'speech_to_text': [{'google': {'language': 'fr-FR'}}],
            'cache_path': '/tmp/kalliope_tts_cache',
            'random_wake_up_answers': ['Oui monsieur?'],
            'default_text_to_speech': 'pico2wave',
            'default_speech_to_text': 'google',
            'random_wake_up_sounds': ['ding.wav', 'dong.wav'],
            'text_to_speech': [
                {'pico2wave': {'cache': True, 'language': 'fr-FR'}},
                {'voxygen': {'voice': 'Agnes', 'cache': True}}
            ],
            'default_synapse': 'Default-synapse',
            'resource_directory':{
                'neuron': "/tmp/kalliope/tests/kalliope_resources_dir/neurons",
                'stt': "/tmp/kalliope/tests/kalliope_resources_dir/stt",
                'tts': "/tmp/kalliope/tests/kalliope_resources_dir/tts",
                'trigger': "/tmp/kalliope/tests/kalliope_resources_dir/trigger"
            }
        }

        # Init the folders, otherwise it raises an exceptions
        os.makedirs("/tmp/kalliope/tests/kalliope_resources_dir/neurons")
        os.makedirs("/tmp/kalliope/tests/kalliope_resources_dir/stt")
        os.makedirs("/tmp/kalliope/tests/kalliope_resources_dir/tts")
        os.makedirs("/tmp/kalliope/tests/kalliope_resources_dir/trigger")

    def tearDown(self):
        # Cleanup
        shutil.rmtree('/tmp/kalliope/tests/kalliope_resources_dir')

        Singleton._instances = {}

    def test_singleton(self):
        s1 = SettingLoader(file_path=self.settings_file_to_test)
        s2 = SettingLoader(file_path=self.settings_file_to_test)

        self.assertTrue(s1.settings is s2.settings)

    def test_get_yaml_config(self):

        sl = SettingLoader(file_path=self.settings_file_to_test)
        self.assertEqual(sl.yaml_config, self.settings_dict)

    def test_get_settings(self):
        settings_object = Settings()
        settings_object.default_tts_name = "pico2wave"
        settings_object.default_stt_name = "google"
        settings_object.default_trigger_name = "snowboy"
        tts1 = Tts(name="pico2wave", parameters={'cache': True, 'language': 'fr-FR'})
        tts2 = Tts(name="voxygen", parameters={'voice': 'Agnes', 'cache': True})
        settings_object.ttss = [tts1, tts2]
        stt = Stt(name="google", parameters={'language': 'fr-FR'})
        settings_object.stts = [stt]
        settings_object.random_wake_up_answers = ['Oui monsieur?']
        settings_object.random_wake_up_sounds = ['ding.wav', 'dong.wav']
        trigger1 = Trigger(name="snowboy",
                           parameters={'pmdl_file': 'trigger/snowboy/resources/kalliope-FR-6samples.pmdl'})
        settings_object.triggers = [trigger1]
        settings_object.rest_api = RestAPI(password_protected=True, active=True,
                                           login="admin", password="secret", port=5000)
        settings_object.cache_path = '/tmp/kalliope_tts_cache'
        settings_object.default_synapse = 'Default-synapse'
        resources = Resources(neuron_folder="/tmp/kalliope/tests/kalliope_resources_dir/neurons",
                              stt_folder="/tmp/kalliope/tests/kalliope_resources_dir/stt",
                              tts_folder="/tmp/kalliope/tests/kalliope_resources_dir/tts",
                              trigger_folder="/tmp/kalliope/tests/kalliope_resources_dir/trigger")

        settings_object.resources=resources
        settings_object.machine = platform.machine()

        sl = SettingLoader(file_path=self.settings_file_to_test)

        self.assertEqual(settings_object, sl.settings)

    def test_get_default_speech_to_text(self):
        expected_default_speech_to_text = "google"
        sl = SettingLoader(file_path=self.settings_file_to_test)

        self.assertEqual(expected_default_speech_to_text, sl._get_default_speech_to_text(self.settings_dict))

    def test_get_default_text_to_speech(self):
        expected_default_text_to_speech = "pico2wave"
        sl = SettingLoader(file_path=self.settings_file_to_test)
        self.assertEqual(expected_default_text_to_speech, sl._get_default_text_to_speech(self.settings_dict))

    def test_get_default_trigger(self):
        expected_default_trigger = "snowboy"
        sl = SettingLoader(file_path=self.settings_file_to_test)
        self.assertEqual(expected_default_trigger, sl._get_default_trigger(self.settings_dict))

    def test_get_stts(self):
        stt = Stt(name="google", parameters={'language': 'fr-FR'})
        sl = SettingLoader(file_path=self.settings_file_to_test)
        self.assertEqual([stt], sl._get_stts(self.settings_dict))

    def test_get_ttss(self):
        tts1 = Tts(name="pico2wave", parameters={'cache': True, 'language': 'fr-FR'})
        tts2 = Tts(name="voxygen", parameters={'voice': 'Agnes', 'cache': True})
        sl = SettingLoader(file_path=self.settings_file_to_test)
        self.assertEqual([tts1, tts2], sl._get_ttss(self.settings_dict))

    def test_get_triggers(self):
        trigger1 = Trigger(name="snowboy",
                           parameters={'pmdl_file': 'trigger/snowboy/resources/kalliope-FR-6samples.pmdl'})
        sl = SettingLoader(file_path=self.settings_file_to_test)
        self.assertEqual([trigger1], sl._get_triggers(self.settings_dict))

    def test_get_random_wake_up_answers(self):
        expected_random_wake_up_answers = ['Oui monsieur?']
        sl = SettingLoader(file_path=self.settings_file_to_test)
        self.assertEqual(expected_random_wake_up_answers, sl._get_random_wake_up_answers(self.settings_dict))

    def test_get_rest_api(self):
        expected_rest_api = RestAPI(password_protected=True, active=True,
                                    login="admin", password="secret", port=5000)

        sl = SettingLoader(file_path=self.settings_file_to_test)
        self.assertEqual(expected_rest_api, sl._get_rest_api(self.settings_dict))

    def test_get_cache_path(self):
        expected_cache_path = '/tmp/kalliope_tts_cache'
        sl = SettingLoader(file_path=self.settings_file_to_test)
        self.assertEqual(expected_cache_path, sl._get_cache_path(self.settings_dict))

    def test_get_default_synapse(self):
        expected_default_synapse = 'Default-synapse'
        sl = SettingLoader(file_path=self.settings_file_to_test)
        self.assertEqual(expected_default_synapse, sl._get_default_synapse(self.settings_dict))

    def test_get_resources(self):

        resources = Resources(neuron_folder="/tmp/kalliope/tests/kalliope_resources_dir/neurons",
                              stt_folder="/tmp/kalliope/tests/kalliope_resources_dir/stt",
                              tts_folder="/tmp/kalliope/tests/kalliope_resources_dir/tts",
                              trigger_folder="/tmp/kalliope/tests/kalliope_resources_dir/trigger")
        expected_resource = resources
        sl = SettingLoader(file_path=self.settings_file_to_test)
        self.assertEquals(expected_resource, sl._get_resources(self.settings_dict))


if __name__ == '__main__':
    unittest.main()
