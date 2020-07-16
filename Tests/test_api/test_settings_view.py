import json

import mock

from Tests.test_api.base import RestAPITestBase


class TestSettingsView(RestAPITestBase):

    def test_get_mute(self):
        """
        Test for api get mute.
        """
        url = self.get_server_url() + "/settings/mute"
        headers = {"Content-Type": "application/json"}

        self.settings.options.mute = False
        result = self.client.get(url, headers=headers)

        expected_content = {
            "mute": False
        }

        self.assertEqual(json.dumps(expected_content, sort_keys=True),
                         json.dumps(json.loads(result.get_data().decode('utf-8')), sort_keys=True))
        self.assertEqual(result.status_code, 200)

    def test_set_mute(self):
        """
        Test for api set mute.
        """
        url = self.get_server_url() + "/settings/mute"
        data = {"mute": "True"}
        headers = {"Content-Type": "application/json"}

        self.settings.options.mute = False
        result = self.client.post(url,
                                  headers=headers,
                                  data=json.dumps(data))

        expected_content = {
            "mute": True
        }

        self.assertEqual(json.dumps(expected_content, sort_keys=True),
                         json.dumps(json.loads(result.get_data().decode('utf-8')), sort_keys=True))
        self.assertEqual(result.status_code, 200)

    def test_get_deaf(self):
        """
        Test for api get deaf.
        """
        url = self.get_server_url() + "/settings/deaf"
        headers = {"Content-Type": "application/json"}

        self.settings.options.deaf = False
        result = self.client.get(url, headers=headers)

        expected_content = {
            "deaf": False
        }

        self.assertEqual(json.dumps(expected_content, sort_keys=True),
                         json.dumps(json.loads(result.get_data().decode('utf-8')), sort_keys=True))
        self.assertEqual(result.status_code, 200)

    def test_set_deaf(self):
        """
        Test for api set deaf.
        """
        url = self.get_server_url() + "/settings/deaf"
        data = {"deaf": "True"}
        headers = {"Content-Type": "application/json"}

        self.settings.options.deaf = False
        with mock.patch("kalliope.core.SignalLauncher.SignalLauncher.get_order_instance") as mock_order:
            result = self.client.post(url,
                                      headers=headers,
                                      data=json.dumps(data))

            expected_content = {
                "deaf": True
            }

            mock_order.assert_called_once()
            self.assertEqual(json.dumps(expected_content, sort_keys=True),
                             json.dumps(json.loads(result.get_data().decode('utf-8')), sort_keys=True))
            self.assertEqual(result.status_code, 200)

    def test_get_recognizer_multiplier(self):
        """
        Test for api get recognizer_multiplier.
        """
        url = self.get_server_url() + "/settings/recognizer_multiplier"
        headers = {"Content-Type": "application/json"}
        self.settings.options.recognizer_multiplier = 3000
        result = self.client.get(url, headers=headers)

        expected_content = {
            "recognizer_multiplier": 3000
        }

        self.assertEqual(json.dumps(expected_content, sort_keys=True),
                         json.dumps(json.loads(result.get_data().decode('utf-8')), sort_keys=True))
        self.assertEqual(result.status_code, 200)

    def test_set_recognizer_multiplier(self):
        """
        Test for api set recognizer_multiplier.
        """
        url = self.get_server_url() + "/settings/recognizer_multiplier"
        data = {"recognizer_multiplier": "6000"}
        headers = {"Content-Type": "application/json"}

        self.settings.recognizer_multiplier = 4000
        result = self.client.post(url,
                                  headers=headers,
                                  data=json.dumps(data))

        expected_content = {
            "recognizer_multiplier": "6000"
        }

        self.assertEqual(json.dumps(expected_content, sort_keys=True),
                         json.dumps(json.loads(result.get_data().decode('utf-8')), sort_keys=True))
        self.assertEqual(result.status_code, 200)

    def test_get_recognizer_energy_ratio(self):
        """
        Test for api get recognizer_energy_ratio second.
        """
        url = self.get_server_url() + "/settings/recognizer_energy_ratio"
        headers = {"Content-Type": "application/json"}
        self.settings.options.recognizer_energy_ratio = 30
        result = self.client.get(url, headers=headers)

        expected_content = {
            "recognizer_energy_ratio": 30
        }

        self.assertEqual(json.dumps(expected_content, sort_keys=True),
                         json.dumps(json.loads(result.get_data().decode('utf-8')), sort_keys=True))
        self.assertEqual(result.status_code, 200)

    def test_set_recognizer_energy_ratio(self):
        """
        Test for api set recognizer_energy_ratio.
        """
        url = self.get_server_url() + "/settings/recognizer_energy_ratio"
        data = {"recognizer_energy_ratio": "60"}
        headers = {"Content-Type": "application/json"}

        self.settings.recognizer_energy_ratio = 40
        result = self.client.post(url,
                                  headers=headers,
                                  data=json.dumps(data))

        expected_content = {
            "recognizer_energy_ratio": "60"
        }

        self.assertEqual(json.dumps(expected_content, sort_keys=True),
                         json.dumps(json.loads(result.get_data().decode('utf-8')), sort_keys=True))
        self.assertEqual(result.status_code, 200)

    def test_get_recognizer_recording_timeout(self):
        """
        Test for api get recognizer_recording_timeout.
        """
        url = self.get_server_url() + "/settings/recognizer_recording_timeout"
        headers = {"Content-Type": "application/json"}
        self.settings.options.recognizer_recording_timeout = 3000
        result = self.client.get(url, headers=headers)

        expected_content = {
            "recognizer_recording_timeout": 3000
        }

        self.assertEqual(json.dumps(expected_content, sort_keys=True),
                         json.dumps(json.loads(result.get_data().decode('utf-8')), sort_keys=True))
        self.assertEqual(result.status_code, 200)

    def test_set_recognizer_recording_timeout(self):
        """
        Test for api set recognizer_recording_timeout.
        """
        url = self.get_server_url() + "/settings/recognizer_recording_timeout"
        data = {"recognizer_recording_timeout": "6000"}
        headers = {"Content-Type": "application/json"}

        self.settings.recognizer_recording_timeout = 4000
        result = self.client.post(url,
                                  headers=headers,
                                  data=json.dumps(data))

        expected_content = {
            "recognizer_recording_timeout": "6000"
        }

        self.assertEqual(json.dumps(expected_content, sort_keys=True),
                         json.dumps(json.loads(result.get_data().decode('utf-8')), sort_keys=True))
        self.assertEqual(result.status_code, 200)

    def test_get_recognizer_recording_timeout_with_silence(self):
        """
        Test for api get recognizer_recording_timeout_with_silence second.
        """
        url = self.get_server_url() + "/settings/recognizer_recording_timeout_with_silence"
        headers = {"Content-Type": "application/json"}
        self.settings.options.recognizer_recording_timeout_with_silence = 30
        result = self.client.get(url, headers=headers)

        expected_content = {
            "recognizer_recording_timeout_with_silence": 30
        }

        self.assertEqual(json.dumps(expected_content, sort_keys=True),
                         json.dumps(json.loads(result.get_data().decode('utf-8')), sort_keys=True))
        self.assertEqual(result.status_code, 200)

    def test_set_recognizer_recording_timeout_with_silence(self):
        """
        Test for api set recognizer_recording_timeout_with_silence.
        """
        url = self.get_server_url() + "/settings/recognizer_recording_timeout_with_silence"
        data = {"recognizer_recording_timeout_with_silence": "60"}
        headers = {"Content-Type": "application/json"}

        self.settings.recognizer_recording_timeout_with_silence = 40
        result = self.client.post(url,
                                  headers=headers,
                                  data=json.dumps(data))

        expected_content = {
            "recognizer_recording_timeout_with_silence": "60"
        }

        self.assertEqual(json.dumps(expected_content, sort_keys=True),
                         json.dumps(json.loads(result.get_data().decode('utf-8')), sort_keys=True))
        self.assertEqual(result.status_code, 200)
        
    def test_get_default_tts(self):
        """
        Test for api get default tts name.
        """
        url = self.get_server_url() + "/settings/default_tts"
        headers = {"Content-Type": "application/json"}
        self.settings.default_tts_name = "test"
        result = self.client.get(url, headers=headers)

        expected_content = {
            "default_tts": "test"
        }

        self.assertEqual(json.dumps(expected_content, sort_keys=True),
                         json.dumps(json.loads(result.get_data().decode('utf-8')), sort_keys=True))
        self.assertEqual(result.status_code, 200)

    def test_set_default_tts(self):
        """
        Test for api set default_tts.
        """
        url = self.get_server_url() + "/settings/default_tts"
        data = {"default_tts": "pico2wave"}
        headers = {"Content-Type": "application/json"}

        self.settings.default_tts_name = "test"
        result = self.client.post(url,
                                  headers=headers,
                                  data=json.dumps(data))

        expected_content = {
            "default_tts": "pico2wave"
        }

        self.assertEqual(json.dumps(expected_content, sort_keys=True),
                         json.dumps(json.loads(result.get_data().decode('utf-8')), sort_keys=True))
        self.assertEqual(result.status_code, 200)

    def test_get_default_stt(self):
        """
        Test for api get default stt name.
        """
        url = self.get_server_url() + "/settings/default_stt"
        headers = {"Content-Type": "application/json"}
        self.settings.default_stt_name = "test"
        result = self.client.get(url, headers=headers)

        expected_content = {
            "default_stt": "test"
        }

        self.assertEqual(json.dumps(expected_content, sort_keys=True),
                         json.dumps(json.loads(result.get_data().decode('utf-8')), sort_keys=True))
        self.assertEqual(result.status_code, 200)

    def test_set_default_stt(self):
        """
        Test for api set default_stt.
        """
        url = self.get_server_url() + "/settings/default_stt"
        data = {"default_stt": "google"}
        headers = {"Content-Type": "application/json"}

        self.settings.default_stt_name = "test"
        result = self.client.post(url,
                                  headers=headers,
                                  data=json.dumps(data))

        expected_content = {
            "default_stt": "google"
        }

        self.assertEqual(json.dumps(expected_content, sort_keys=True),
                         json.dumps(json.loads(result.get_data().decode('utf-8')), sort_keys=True))
        self.assertEqual(result.status_code, 200)

    def test_get_default_player(self):
        """
        Test for api get default player.
        """
        url = self.get_server_url() + "/settings/default_player"
        headers = {"Content-Type": "application/json"}
        self.settings.default_player_name = "test"
        result = self.client.get(url, headers=headers)

        expected_content = {
            "default_player": "test"
        }

        self.assertEqual(json.dumps(expected_content, sort_keys=True),
                         json.dumps(json.loads(result.get_data().decode('utf-8')), sort_keys=True))
        self.assertEqual(result.status_code, 200)

    def test_set_default_player(self):
        """
        Test for api set default_player.
        """
        url = self.get_server_url() + "/settings/default_player"
        data = {"default_player": "mplayer"}
        headers = {"Content-Type": "application/json"}

        self.settings.default_player_name = "test"
        result = self.client.post(url,
                                  headers=headers,
                                  data=json.dumps(data))

        expected_content = {
            "default_player": "mplayer"
        }

        self.assertEqual(json.dumps(expected_content, sort_keys=True),
                         json.dumps(json.loads(result.get_data().decode('utf-8')), sort_keys=True))
        self.assertEqual(result.status_code, 200)

    def test_get_default_trigger(self):
        """
        Test for api get default trigger.
        """
        url = self.get_server_url() + "/settings/default_trigger"
        headers = {"Content-Type": "application/json"}
        self.settings.default_trigger_name = "test"
        result = self.client.get(url, headers=headers)

        expected_content = {
            "default_trigger": "test"
        }

        self.assertEqual(json.dumps(expected_content, sort_keys=True),
                         json.dumps(json.loads(result.get_data().decode('utf-8')), sort_keys=True))
        self.assertEqual(result.status_code, 200)

    def test_set_default_trigger(self):
        """
        Test for api set default_trigger.
        """
        url = self.get_server_url() + "/settings/default_trigger"
        data = {"default_trigger": "snowboy"}
        headers = {"Content-Type": "application/json"}

        self.settings.default_trigger_name = "test"
        result = self.client.post(url,
                                  headers=headers,
                                  data=json.dumps(data))

        expected_content = {
            "default_trigger": "snowboy"
        }

        self.assertEqual(json.dumps(expected_content, sort_keys=True),
                         json.dumps(json.loads(result.get_data().decode('utf-8')), sort_keys=True))
        self.assertEqual(result.status_code, 200)

    def test_get_hooks(self):
        """
        Test for api get hooks.
        """
        url = self.get_server_url() + "/settings/hooks"
        headers = {"Content-Type": "application/json"}
        self.settings.hooks = {
            "on_start": "on-start-synapse",
            "on_waiting_for_trigger": {},
            "on_triggered": "on-triggered-synapse",
            "on_start_listening": {},
            "on_stop_listening": {},
            "on_order_found": {},
            "on_order_not_found": "order-not-found-synapse",
            "on_processed_synapses": {},
            "on_deaf": {},
            "on_undeaf": {},
            "on_start_speaking": {},
            "on_stop_speaking": {},
            "on_stt_error": {}
        }
        result = self.client.get(url, headers=headers)

        expected_content = {
            "hooks": {
                "on_start": "on-start-synapse",
                "on_waiting_for_trigger": {},
                "on_triggered": "on-triggered-synapse",
                "on_start_listening": {},
                "on_stop_listening": {},
                "on_order_found": {},
                "on_order_not_found": "order-not-found-synapse",
                "on_processed_synapses": {},
                "on_deaf": {},
                "on_undeaf": {},
                "on_start_speaking": {},
                "on_stop_speaking": {},
                "on_stt_error": {}
            }
        }

        self.assertEqual(json.dumps(expected_content, sort_keys=True),
                         json.dumps(json.loads(result.get_data().decode('utf-8')), sort_keys=True))
        self.assertEqual(result.status_code, 200)

    def test_set_hooks(self):
        """
        Test for api set hooks.
        """
        url = self.get_server_url() + "/settings/hooks"
        data = {"on_waiting_for_trigger": "synapse"}
        headers = {"Content-Type": "application/json"}

        self.settings.hooks = {
            "on_start": "on-start-synapse",
            "on_waiting_for_trigger": {},
            "on_triggered": "on-triggered-synapse",
            "on_start_listening": {},
            "on_stop_listening": {},
            "on_order_found": {},
            "on_order_not_found": "order-not-found-synapse",
            "on_processed_synapses": {},
            "on_deaf": {},
            "on_undeaf": {},
            "on_start_speaking": {},
            "on_stop_speaking": {},
            "on_stt_error": {}
        }

        result = self.client.post(url,
                                  headers=headers,
                                  data=json.dumps(data))

        expected_content = {
            "hooks": {
                "on_start": "on-start-synapse",
                "on_waiting_for_trigger": "synapse",
                "on_triggered": "on-triggered-synapse",
                "on_start_listening": {},
                "on_stop_listening": {},
                "on_order_found": {},
                "on_order_not_found": "order-not-found-synapse",
                "on_processed_synapses": {},
                "on_deaf": {},
                "on_undeaf": {},
                "on_start_speaking": {},
                "on_stop_speaking": {},
                "on_stt_error": {}
            }
        }

        self.assertEqual(json.dumps(expected_content, sort_keys=True),
                         json.dumps(json.loads(result.get_data().decode('utf-8')), sort_keys=True))
        self.assertEqual(result.status_code, 200)

    def test_get_variables(self):
        """
        Test for api get variables.
        """
        url = self.get_server_url() + "/settings/variables"
        headers = {"Content-Type": "application/json"}
        self.settings.variables = {
            "test": "tust",
            "tost": "tist"
        }
        result = self.client.get(url, headers=headers)

        expected_content = {
            "variables": {
                "test": "tust",
                "tost": "tist"
            }
        }

        self.assertEqual(json.dumps(expected_content, sort_keys=True),
                         json.dumps(json.loads(result.get_data().decode('utf-8')), sort_keys=True))
        self.assertEqual(result.status_code, 200)

    def test_set_variables(self):
        """
        Test for api set variables.
        """
        url = self.get_server_url() + "/settings/variables"
        data = {"toto": "titi"}
        headers = {"Content-Type": "application/json"}

        self.settings.variables = {
            "tt": "aa",
            "uu": "ii"
        }

        result = self.client.post(url,
                                  headers=headers,
                                  data=json.dumps(data))

        expected_content = {
            "variables": {
                "tt": "aa",
                "uu": "ii",
                "toto": "titi"
            }
        }

        self.assertEqual(json.dumps(expected_content, sort_keys=True),
                         json.dumps(json.loads(result.get_data().decode('utf-8')), sort_keys=True))
        self.assertEqual(result.status_code, 200)
