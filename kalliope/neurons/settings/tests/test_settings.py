import tempfile
import unittest
import mock

from kalliope.core.Models import Singleton
from kalliope.core.Models.settings.Player import Player
from kalliope.core.Models.settings.Stt import Stt
from kalliope.core.Models.settings.Trigger import Trigger
from kalliope.core.Models.settings.Tts import Tts
from kalliope.neurons.settings import Settings


class TestSettings(unittest.TestCase):

    def setUp(self):
        self.neuron_settings = Settings()

    def tearDown(self):
        # Cleaning for settings singleton
        Singleton._instances = {}

    def test_is_parameters_ok(self):
        # TODO this code relies on the current settings.yml file, should create a full mock instead

        # tts
        self.neuron_settings.default_tts = "pico2wave"
        self.assertTrue(self.neuron_settings._is_parameters_ok())

        self.neuron_settings.text_to_speech = [{"pico2wave": {"language": "fr-FR"}}]
        self.assertTrue(self.neuron_settings._is_parameters_ok())

        # stt
        self.neuron_settings.default_stt = "google"
        self.assertTrue(self.neuron_settings._is_parameters_ok())

        self.neuron_settings.speech_to_text = [{"google": {"language": "fr-FR"}}]
        self.assertTrue(self.neuron_settings._is_parameters_ok())

        # player
        self.neuron_settings.default_player = "mplayer"
        self.assertTrue(self.neuron_settings._is_parameters_ok())

        self.neuron_settings.players = [{"mplayer": {}}]

        # trigger
        self.neuron_settings.default_trigger = "snowboy"
        self.assertTrue(self.neuron_settings._is_parameters_ok())

        # hooks
        self.neuron_settings.hooks = {"blabla": ["coucou", "test"]}
        self.assertTrue(self.neuron_settings._is_parameters_ok())
        self.neuron_settings.hooks = {"blabla": "string"}
        self.assertTrue(self.neuron_settings._is_parameters_ok())

        # variables
        tmpfile = tempfile.NamedTemporaryFile()
        self.neuron_settings.var_files = [tmpfile.name]
        self.assertTrue(self.neuron_settings._is_parameters_ok())

        # deaf
        self.neuron_settings.deaf = 60
        self.assertFalse(self.neuron_settings._is_parameters_ok())
        self.neuron_settings.deaf = "randomString"
        self.assertFalse(self.neuron_settings._is_parameters_ok())
        self.neuron_settings.deaf = 0
        self.assertFalse(self.neuron_settings._is_parameters_ok())
        self.neuron_settings.deaf = True
        self.assertTrue(self.neuron_settings._is_parameters_ok())


        # mute
        self.neuron_settings.mute = 60
        self.assertFalse(self.neuron_settings._is_parameters_ok())
        self.neuron_settings.mute = "randomString"
        self.assertFalse(self.neuron_settings._is_parameters_ok())
        self.neuron_settings.mute = 0
        self.assertFalse(self.neuron_settings._is_parameters_ok())
        self.neuron_settings.mute = True
        self.assertTrue(self.neuron_settings._is_parameters_ok())

        # threshold
        self.neuron_settings.energy_threshold = "randomString"
        self.assertFalse(self.neuron_settings._is_parameters_ok())
        self.neuron_settings.energy_threshold = 60
        self.assertTrue(self.neuron_settings._is_parameters_ok())

        # adjust_ambiant
        self.neuron_settings.adjust_for_ambient_noise_second = "randomString"
        self.assertFalse(self.neuron_settings._is_parameters_ok())
        self.neuron_settings.adjust_for_ambient_noise_second = 60
        self.assertTrue(self.neuron_settings._is_parameters_ok())

    def test_set_settings(self):
        # tts
        self.neuron_settings.default_tts = "randomtts"
        with mock.patch("kalliope.core.ConfigurationManager.SettingEditor.set_default_tts") as mock_setting_editor:
            self.neuron_settings._set_settings()
            mock_setting_editor.assert_called_once_with(self.neuron_settings.default_tts)

        self.neuron_settings.text_to_speech = [{"randomTTS": {"language": "fr-FR"}}]
        tts = Tts(name= "randomTTS", parameters= {"language": "fr-FR"})
        with mock.patch("kalliope.core.ConfigurationManager.SettingEditor.set_ttss") as mock_setting_editor:
            self.neuron_settings._set_settings()
            mock_setting_editor.assert_called_once_with(tts)

        # stt
        self.neuron_settings.default_stt = "randomstt"
        with mock.patch("kalliope.core.ConfigurationManager.SettingEditor.set_default_stt") as mock_setting_editor:
            self.neuron_settings._set_settings()
            mock_setting_editor.assert_called_once_with(self.neuron_settings.default_stt)

        self.neuron_settings.speech_to_text = [{"randomStt": {"language": "fr-FR"}}]
        stt = Stt(name="randomStt", parameters={"language": "fr-FR"})
        with mock.patch("kalliope.core.ConfigurationManager.SettingEditor.set_stts") as mock_setting_editor:
            self.neuron_settings._set_settings()
            mock_setting_editor.assert_called_once_with(stt)

        # players
        self.neuron_settings.default_player = "randomPlayer"
        with mock.patch("kalliope.core.ConfigurationManager.SettingEditor.set_default_player") as mock_setting_editor:
            self.neuron_settings._set_settings()
            mock_setting_editor.assert_called_once_with(self.neuron_settings.default_player)

        self.neuron_settings.players = [{"randomPlayer": {}}]
        player = Player(name="randomPlayer", parameters={})
        with mock.patch("kalliope.core.ConfigurationManager.SettingEditor.set_players") as mock_setting_editor:
            self.neuron_settings._set_settings()
            mock_setting_editor.assert_called_once_with(player)

        # triggers
        self.neuron_settings.default_trigger = "randomTrigger"
        with mock.patch("kalliope.core.ConfigurationManager.SettingEditor.set_default_trigger") as mock_setting_editor:
            self.neuron_settings._set_settings()
            mock_setting_editor.assert_called_once_with(self.neuron_settings.default_trigger)

        self.neuron_settings.triggers = [{"randomTrigger": {}}]
        trigger = Trigger(name="randomTrigger", parameters={})
        with mock.patch("kalliope.core.ConfigurationManager.SettingEditor.set_trigger") as mock_setting_editor:
            self.neuron_settings._set_settings()
            mock_setting_editor.assert_called_once_with(trigger)

        # Hooks
        self.neuron_settings.hooks = {"randomHook": "randomSynapse"}
        with mock.patch("kalliope.core.ConfigurationManager.SettingEditor.set_hooks") as mock_setting_editor:
            self.neuron_settings._set_settings()
            mock_setting_editor.assert_called_once_with(self.neuron_settings.hooks)

        # Variables
        with tempfile.NamedTemporaryFile() as tmpfile:
            tmpfile.write("coucou: 'hello'".encode()) # encode to get the binary format
            tmpfile.flush() # To refresh the file with the data
            self.neuron_settings.var_files = [tmpfile.name]
            with mock.patch("kalliope.core.ConfigurationManager.SettingEditor.set_variables") as mock_setting_editor:
                self.neuron_settings._set_settings()
                mock_setting_editor.assert_called_once_with({'coucou': 'hello'})
                self.neuron_settings.var_files = [] # reset var_file

        # Deaf
        self.neuron_settings.deaf = True
        with mock.patch("kalliope.core.ConfigurationManager.SettingEditor.set_deaf_status") as mock_setting_editor:
            with mock.patch("kalliope.core.SignalLauncher.SignalLauncher.get_order_instance"):
                self.neuron_settings._set_settings()
                mock_setting_editor.assert_called_once()

        # Mute
        self.neuron_settings.mute = True
        with mock.patch("kalliope.core.ConfigurationManager.SettingEditor.set_mute_status") as mock_setting_editor:
            self.neuron_settings._set_settings()
            mock_setting_editor.assert_called_once_with(True)

        # set_energy_threshold
        self.neuron_settings.energy_threshold = 50
        with mock.patch("kalliope.core.ConfigurationManager.SettingEditor.set_energy_threshold") as mock_setting_editor:
            self.neuron_settings._set_settings()
            mock_setting_editor.assert_called_once_with(50)

        # set_adjust_for_ambient_noise_second
        self.neuron_settings.adjust_for_ambient_noise_second = 3000
        with mock.patch(
                "kalliope.core.ConfigurationManager.SettingEditor.set_adjust_for_ambient_noise_second") as mock_setting_editor:
            self.neuron_settings._set_settings()
            mock_setting_editor.assert_called_once_with(3000)