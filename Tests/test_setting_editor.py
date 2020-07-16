import inspect
import os
import shutil
import unittest

import mock

from kalliope import SettingLoader
from kalliope.core.ConfigurationManager import SettingEditor
from kalliope.core.Models.settings.Player import Player
from kalliope.core.Models.settings.Stt import Stt
from kalliope.core.Models.settings.Trigger import Trigger
from kalliope.core.Models.settings.Tts import Tts


class TestSettingEditor(unittest.TestCase):
    """
    Test class for the ~SettingEditor class and methods
    """

    def setUp(self):
        # get current script directory path. We are in /an/unknown/path/kalliope/core/tests
        cur_script_directory = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        # get parent dir. Now we are in /an/unknown/path/kalliope
        root_dir = os.path.normpath(cur_script_directory + os.sep + os.pardir)

        self.settings_file_to_test = root_dir + os.sep + "Tests/settings/settings_test.yml"

        # Init the folders, otherwise it raises an exceptions
        os.makedirs("/tmp/kalliope/tests/kalliope_resources_dir/neurons")
        os.makedirs("/tmp/kalliope/tests/kalliope_resources_dir/stt")
        os.makedirs("/tmp/kalliope/tests/kalliope_resources_dir/tts")
        os.makedirs("/tmp/kalliope/tests/kalliope_resources_dir/trigger")

        self.sl = SettingLoader(file_path=self.settings_file_to_test)

    def tearDown(self):
        # Cleanup
        shutil.rmtree('/tmp/kalliope/tests/kalliope_resources_dir')

    def test_set_mute_status(self):
        with mock.patch("kalliope.core.ConfigurationManager.SettingLoader") as mock_setting_loader:
            mock_setting_loader.return_value(self.sl)
            SettingEditor.set_mute_status(mute=True)
            self.assertTrue(self.sl.settings.options.mute)

    def test_set_deaf_status(self):
        with mock.patch("kalliope.core.ConfigurationManager.SettingLoader") as mock_setting_loader:
            mock_setting_loader.return_value(self.sl)
            SettingEditor.set_deaf_status(mock.Mock(), deaf=False)
            self.assertFalse(self.sl.settings.options.deaf)

    def test_set_recognizer_multiplier(self):
        with mock.patch("kalliope.core.ConfigurationManager.SettingLoader") as mock_setting_loader:
            mock_setting_loader.return_value(self.sl)
            SettingEditor.set_recognizer_multiplier(600)
            self.assertEqual(600, self.sl.settings.options.recognizer_multiplier)

    def test_set_recognizer_energy_ratio(self):
        with mock.patch("kalliope.core.ConfigurationManager.SettingLoader") as mock_setting_loader:
            mock_setting_loader.return_value(self.sl)
            SettingEditor.set_recognizer_energy_ratio(600)
            self.assertEqual(600, self.sl.settings.options.recognizer_energy_ratio)
    
    def test_set_recognizer_recording_timeout(self):
        with mock.patch("kalliope.core.ConfigurationManager.SettingLoader") as mock_setting_loader:
            mock_setting_loader.return_value(self.sl)
            SettingEditor.set_recognizer_recording_timeout(600)
            self.assertEqual(600, self.sl.settings.options.recognizer_recording_timeout)

    def test_set_recognizer_recording_timeout_with_silence(self):
        with mock.patch("kalliope.core.ConfigurationManager.SettingLoader") as mock_setting_loader:
            mock_setting_loader.return_value(self.sl)
            SettingEditor.set_recognizer_recording_timeout_with_silence(600)
            self.assertEqual(600, self.sl.settings.options.recognizer_recording_timeout_with_silence)

    def test_set_default_player(self):
        default_name = "NamePlayer"
        with mock.patch("kalliope.core.ConfigurationManager.SettingLoader") as mock_setting_loader:
            mock_setting_loader.return_value(self.sl)
            SettingEditor.set_default_player(default_name)
            self.assertEqual("mplayer", self.sl.settings.default_player_name)  # not existing in the list, not updated !
            default_name = "pyalsaaudio"
            SettingEditor.set_default_player(default_name)
            self.assertEqual(default_name, self.sl.settings.default_player_name)  # Updated

    def test_set_players(self):
        new_player = Player(name="totoplayer", parameters={})
        with mock.patch("kalliope.core.ConfigurationManager.SettingLoader") as mock_setting_loader:
            mock_setting_loader.return_value(self.sl)
            SettingEditor.set_players(new_player)
            self.assertIn(new_player, self.sl.settings.players)

    def test_set_default_trigger(self):
        default_name = "NameTrigger"
        with mock.patch("kalliope.core.ConfigurationManager.SettingLoader") as mock_setting_loader:
            mock_setting_loader.return_value(self.sl)
            SettingEditor.set_default_trigger(default_name)
            self.assertEqual("snowboy",
                             self.sl.settings.default_trigger_name)  # not existing in the list, not updated !
            default_name = "snowboy"
            SettingEditor.set_default_trigger(default_name)
            self.assertEqual(default_name, self.sl.settings.default_trigger_name)

    def test_set_triggers(self):
        new_trigger = Trigger(name="tototrigger", parameters={})
        with mock.patch("kalliope.core.ConfigurationManager.SettingLoader") as mock_setting_loader:
            mock_setting_loader.return_value(self.sl)
            SettingEditor.set_trigger(new_trigger)
            self.assertIn(new_trigger, self.sl.settings.triggers)

    def test_set_default_stt(self):
        default_name = "NameStt"
        with mock.patch("kalliope.core.ConfigurationManager.SettingLoader") as mock_setting_loader:
            mock_setting_loader.return_value(self.sl)
            SettingEditor.set_default_stt(default_name)
            self.assertEqual("google", self.sl.settings.default_stt_name) # not updated because not in the list
            default_name = "google"
            SettingEditor.set_default_stt(default_name)
            self.assertEqual(default_name, self.sl.settings.default_stt_name) # updated

    def test_set_stts(self):
        new_stt = Stt(name="totoStt", parameters={})
        with mock.patch("kalliope.core.ConfigurationManager.SettingLoader") as mock_setting_loader:
            mock_setting_loader.return_value(self.sl)
            SettingEditor.set_stts(new_stt)
            self.assertIn(new_stt, self.sl.settings.stts)

    def test_set_default_tts(self):
        default_name = "NameTts"
        with mock.patch("kalliope.core.ConfigurationManager.SettingLoader") as mock_setting_loader:
            mock_setting_loader.return_value(self.sl)
            SettingEditor.set_default_tts(default_name)
            self.assertEqual("pico2wave", self.sl.settings.default_tts_name)
            default_name = "googletts"
            SettingEditor.set_default_tts(default_name)
            self.assertEqual(default_name, self.sl.settings.default_tts_name)

    def test_set_ttss(self):
        new_tts = Tts(name="totoTss", parameters={})
        with mock.patch("kalliope.core.ConfigurationManager.SettingLoader") as mock_setting_loader:
            mock_setting_loader.return_value(self.sl)
            SettingEditor.set_ttss(new_tts)
            self.assertIn(new_tts, self.sl.settings.ttss)

    def test_set_hooks(self):
        default_hooks = {"on_deaf": "randomSynapse"}
        with mock.patch("kalliope.core.ConfigurationManager.SettingLoader") as mock_setting_loader:
            mock_setting_loader.return_value(self.sl)
            SettingEditor.set_hooks(default_hooks)
            self.assertEqual("randomSynapse", self.sl.settings.hooks["on_deaf"])
            # self.assertTrue(set(default_hooks.items()).issubset(set(self.sl.settings.hooks))) # Not working for non hashable values

    def test_set_variabless(self):
        default_variables = {"coucou": "hello"}
        with mock.patch("kalliope.core.ConfigurationManager.SettingLoader") as mock_setting_loader:
            mock_setting_loader.return_value(self.sl)
            SettingEditor.set_variables(default_variables)
            self.assertEqual("hello", self.sl.settings.variables["coucou"])
