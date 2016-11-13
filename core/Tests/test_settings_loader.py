import platform
import unittest

from core.ConfigurationManager import SettingLoader
from core.Models.RestAPI import RestAPI
from core.Models.Settings import Settings
from core.Models.Stt import Stt
from core.Models.Trigger import Trigger
from core.Models.Tts import Tts


class TestSettingsoader(unittest.TestCase):

    def setUp(self):
        self.settings_file_to_test = "core/Tests/settings/settings_test.yml"

        self.settings_dict = {
            'rest_api':
                {'active': True, 'login': 'admin', 'password': 'secret',
                 'password_protected': True, 'port': 5000},
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
            ]
        }

    def test_singleton(self):
        s1 = SettingLoader.Instance(file_path=self.settings_file_to_test)
        s2 = SettingLoader.Instance(file_path=self.settings_file_to_test)

        self.assertTrue(s1.settings == s2.settings)

    def test_get_yaml_config(self):

        sl = SettingLoader.Instance(file_path=self.settings_file_to_test)

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
        settings_object.machine = platform.machine()

        sl = SettingLoader.Instance(file_path=self.settings_file_to_test)

        self.assertEqual(settings_object, sl.settings)

    def test_get_default_speech_to_text(self):
        expected_default_speech_to_text = "google"
        sl = SettingLoader.Instance(file_path=self.settings_file_to_test)

        self.assertEqual(expected_default_speech_to_text, sl._get_default_speech_to_text(self.settings_dict))

    def test_get_default_text_to_speech(self):
        expected_default_text_to_speech = "pico2wave"
        sl = SettingLoader.Instance(file_path=self.settings_file_to_test)

        self.assertEqual(expected_default_text_to_speech, sl._get_default_text_to_speech(self.settings_dict))

    def test_get_default_trigger(self):
        expected_default_trigger = "snowboy"
        sl = SettingLoader.Instance(file_path=self.settings_file_to_test)

        self.assertEqual(expected_default_trigger, sl._get_default_trigger(self.settings_dict))

    def test_get_stts(self):
        stt = Stt(name="google", parameters={'language': 'fr-FR'})
        sl = SettingLoader.Instance(file_path=self.settings_file_to_test)
        self.assertEqual([stt], sl._get_stts(self.settings_dict))

    def test_get_ttss(self):
        tts1 = Tts(name="pico2wave", parameters={'cache': True, 'language': 'fr-FR'})
        tts2 = Tts(name="voxygen", parameters={'voice': 'Agnes', 'cache': True})
        sl = SettingLoader.Instance(file_path=self.settings_file_to_test)
        self.assertEqual([tts1, tts2], sl._get_ttss(self.settings_dict))

    def test_get_triggers(self):
        trigger1 = Trigger(name="snowboy",
                           parameters={'pmdl_file': 'trigger/snowboy/resources/kalliope-FR-6samples.pmdl'})
        sl = SettingLoader.Instance(file_path=self.settings_file_to_test)
        self.assertEqual([trigger1], sl._get_triggers(self.settings_dict))

    def test_get_random_wake_up_answers(self):
        expected_random_wake_up_answers = ['Oui monsieur?']
        sl = SettingLoader.Instance(file_path=self.settings_file_to_test)
        self.assertEqual(expected_random_wake_up_answers, sl._get_random_wake_up_answers(self.settings_dict))

    def test_get_rest_api(self):
        expected_rest_api = RestAPI(password_protected=True, active=True,
                                    login="admin", password="secret", port=5000)

        sl = SettingLoader.Instance(file_path=self.settings_file_to_test)
        self.assertEqual(expected_rest_api, sl._get_rest_api(self.settings_dict))

    def test_get_cache_path(self):
        expected_cache_path = '/tmp/kalliope_tts_cache'
        sl = SettingLoader.Instance(file_path=self.settings_file_to_test)
        self.assertEqual(expected_cache_path, sl._get_cache_path(self.settings_dict))

if __name__ == '__main__':
    unittest.main()
