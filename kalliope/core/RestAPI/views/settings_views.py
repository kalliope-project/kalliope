import logging

from flask import jsonify, Blueprint
from flask import request

from kalliope import SignalLauncher
from kalliope.core.ConfigurationManager import SettingEditor
from kalliope.core.RestAPI import utils
from kalliope.core.RestAPI.utils import requires_auth

logging.basicConfig()
logger = logging.getLogger("kalliope")

UPLOAD_FOLDER = '/tmp/kalliope/tmp_uploaded_audio'
ALLOWED_EXTENSIONS = {'wav'}


class SettingsView(Blueprint):
    def __init__(self, name, import_name, app=None, brain=None, settings=None):
        self.brain = brain
        self.settings = settings
        self.app = app
        super(SettingsView, self).__init__(name, import_name)
        self.add_url_rule('/settings', view_func=self.get_current_settings, methods=['GET'])
        self.add_url_rule('/settings/deaf/', view_func=self.get_deaf, methods=['GET'])
        self.add_url_rule('/settings/deaf/', view_func=self.set_deaf, methods=['POST'])
        self.add_url_rule('/settings/mute/', view_func=self.get_mute, methods=['GET'])
        self.add_url_rule('/settings/mute/', view_func=self.set_mute, methods=['POST'])
        self.add_url_rule('/settings/recognizer_multiplier/', view_func=self.get_recognizer_multiplier,
                          methods=['GET'])
        self.add_url_rule('/settings/recognizer_multiplier/', view_func=self.set_recognizer_multiplier,
                          methods=['POST'])
        self.add_url_rule('/settings/recognizer_energy_ratio/', view_func=self.get_recognizer_energy_ratio,
                          methods=['GET'])
        self.add_url_rule('/settings/recognizer_energy_ratio/', view_func=self.set_recognizer_energy_ratio,
                          methods=['POST'])
        self.add_url_rule('/settings/recognizer_recording_timeout/', view_func=self.get_recognizer_recording_timeout,
                          methods=['GET'])
        self.add_url_rule('/settings/recognizer_recording_timeout/', view_func=self.set_recognizer_recording_timeout,
                          methods=['POST'])
        self.add_url_rule('/settings/recognizer_recording_timeout_with_silence/', view_func=self.get_recognizer_recording_timeout_with_silence,
                          methods=['GET'])
        self.add_url_rule('/settings/recognizer_recording_timeout_with_silence/', view_func=self.set_recognizer_recording_timeout_with_silence,
                          methods=['POST'])
        self.add_url_rule('/settings/default_tts/', view_func=self.get_default_tts,
                          methods=['GET'])
        self.add_url_rule('/settings/default_tts/', view_func=self.set_default_tts,
                          methods=['POST'])
        self.add_url_rule('/settings/default_stt/', view_func=self.get_default_stt,
                          methods=['GET'])
        self.add_url_rule('/settings/default_stt/', view_func=self.set_default_stt,
                          methods=['POST'])
        self.add_url_rule('/settings/default_player/', view_func=self.get_default_player,
                          methods=['GET'])
        self.add_url_rule('/settings/default_player/', view_func=self.set_default_player,
                          methods=['POST'])
        self.add_url_rule('/settings/default_trigger/', view_func=self.get_default_trigger,
                          methods=['GET'])
        self.add_url_rule('/settings/default_trigger/', view_func=self.set_default_trigger,
                          methods=['POST'])
        self.add_url_rule('/settings/hooks/', view_func=self.get_hooks,
                          methods=['GET'])
        self.add_url_rule('/settings/hooks/', view_func=self.set_hooks,
                          methods=['POST'])
        self.add_url_rule('/settings/variables/', view_func=self.get_variables,
                          methods=['GET'])
        self.add_url_rule('/settings/variables/', view_func=self.set_variables,
                          methods=['POST'])

    @requires_auth
    def get_deaf(self):
        """
        Return the current trigger status

        Curl test
        curl -i --user admin:secret  -X GET  http://127.0.0.1:5000/deaf
        """

        # find the order signal and call the deaf settings
        if self.settings.options.deaf is not None:
            data = {
                "deaf": self.settings.options.deaf
            }
            return jsonify(data), 200

        # if no Order instance
        data = {
            "error": "deaf status unknow"
        }
        return jsonify(error=data), 400

    @requires_auth
    def set_deaf(self):
        """
        Set the trigger status (deaf or not)

        Curl test:
        curl -i -H "Content-Type: application/json" --user admin:secret  -X POST \
        -d '{"deaf": "True"}' http://127.0.0.1:5000/deaf
        """

        if not request.get_json() or 'deaf' not in request.get_json():
            data = {
                "Error": "Wrong parameters, 'deaf' not set"
            }
            return jsonify(error=data), 400

        # get deaf if present
        deaf = utils.get_value_flag_from_request(http_request=request,
                                                 flag_to_find="deaf",
                                                 is_boolean=True)

        signal_order = SignalLauncher.get_order_instance()
        if signal_order is not None and deaf is not None and self.settings.options.deaf is not None:
            SettingEditor.set_deaf_status(signal_order.trigger_instance, deaf)
            data = {
                "deaf": self.settings.options.deaf
            }
            return jsonify(data), 200

        data = {
            "error": "Cannot switch deaf status"
        }
        return jsonify(error=data), 400

    @requires_auth
    def get_mute(self):
        """
        Return the current mute status

        Curl test
        curl -i --user admin:secret  -X GET  http://127.0.0.1:5000/mute
        """

        # find the order signal and call the mute settings
        if self.settings.options.mute is not None:
            data = {
                "mute": self.settings.options.mute
            }
            return jsonify(data), 200

        # if no Order instance
        data = {
            "error": "mute status unknow"
        }
        return jsonify(error=data), 400

    @requires_auth
    def set_mute(self):
        """
        Set the Kalliope Core mute status (mute or not)

        Curl test:
        curl -i -H "Content-Type: application/json" --user admin:secret  -X POST \
        -d '{"mute": "True"}' http://127.0.0.1:5000/mute
        """

        if not request.get_json() or 'mute' not in request.get_json():
            data = {
                "Error": "Wrong parameters, 'mute' not set"
            }
            return jsonify(error=data), 400

        # get mute if present
        mute = utils.get_value_flag_from_request(http_request=request,
                                                 flag_to_find="mute",
                                                 is_boolean=True)
        SettingEditor.set_mute_status(mute=mute)

        data = {
            "mute": mute
        }
        return jsonify(data), 200

    @requires_auth
    def get_recognizer_multiplier(self):
        """
        Return the current recognizer_multiplier value from settings

        Curl test
        curl -i --user admin:secret  -X GET  http://127.0.0.1:5000/settings/recognizer_multiplier
        """

        if self.settings.options.recognizer_multiplier is not None:
            data = {
                "recognizer_multiplier": self.settings.options.recognizer_multiplier
            }
            return jsonify(data), 200

        # if no Order instance
        data = {
            "error": "recognizer_multiplier status not defined"
        }
        return jsonify(error=data), 400

    @requires_auth
    def set_recognizer_multiplier(self):
        """
        Set the Kalliope Core recognizer_multiplier value

        Curl test:
        curl -i -H "Content-Type: application/json" --user admin:secret  -X POST \
        -d '{"recognizer_multiplier": "6666"}' http://127.0.0.1:5000/settings/recognizer_multiplier
        """

        if not request.get_json() or 'recognizer_multiplier' not in request.get_json():
            data = {
                "Error": "Wrong parameters, 'recognizer_multiplier' not set"
            }
            return jsonify(error=data), 400

        # get recognizer_multiplier if present
        recognizer_multiplier = utils.get_value_flag_from_request(http_request=request,
                                                                  flag_to_find="recognizer_multiplier",
                                                                  is_boolean=False)

        SettingEditor.set_recognizer_multiplier(recognizer_multiplier=recognizer_multiplier)

        data = {
            "recognizer_multiplier": recognizer_multiplier
        }
        return jsonify(data), 200

    @requires_auth
    def get_recognizer_energy_ratio(self):
        """
        Return the current recognizer_energy_ratio value from settings

        Curl test
        curl -i --user admin:secret  -X GET  http://127.0.0.1:5000/settings/recognizer_energy_ratio
        """

        if self.settings.options.recognizer_energy_ratio is not None:
            data = {
                "recognizer_energy_ratio": self.settings.options.recognizer_energy_ratio
            }
            return jsonify(data), 200

        # if no Order instance
        data = {
            "error": "recognizer_energy_ratio status not defined"
        }
        return jsonify(error=data), 400

    @requires_auth
    def set_recognizer_energy_ratio(self):
        """
        Set the Kalliope Core recognizer_energy_ratio value

        Curl test:
        curl -i -H "Content-Type: application/json" --user admin:secret  -X POST \
        -d '{"energy_threshold": "6666"}' http://127.0.0.1:5000/settings/recognizer_energy_ratio
        """

        if not request.get_json() or 'recognizer_energy_ratio' not in request.get_json():
            data = {
                "Error": "Wrong parameters, 'recognizer_energy_ratio' not set"
            }
            return jsonify(error=data), 400

        # get if present
        recognizer_energy_ratio = utils.get_value_flag_from_request(http_request=request,
                                                                    flag_to_find="recognizer_energy_ratio",
                                                                    is_boolean=False)

        SettingEditor.set_recognizer_energy_ratio(recognizer_energy_ratio=recognizer_energy_ratio)

        data = {
            "recognizer_energy_ratio": recognizer_energy_ratio
        }
        return jsonify(data), 200

    @requires_auth
    def get_recognizer_recording_timeout(self):
        """
        Return the current recognizer_recording_timeout value from settings

        Curl test
        curl -i --user admin:secret  -X GET  http://127.0.0.1:5000/settings/recognizer_recording_timeout
        """

        if self.settings.options.recognizer_recording_timeout is not None:
            data = {
                "recognizer_recording_timeout": self.settings.options.recognizer_recording_timeout
            }
            return jsonify(data), 200

        # if no Order instance
        data = {
            "error": "recognizer_recording_timeout status not defined"
        }
        return jsonify(error=data), 400

    @requires_auth
    def set_recognizer_recording_timeout(self):
        """
        Set the Kalliope Core recognizer_recording_timeout value

        Curl test:
        curl -i -H "Content-Type: application/json" --user admin:secret  -X POST \
        -d '{"energy_threshold": "6666"}' http://127.0.0.1:5000/settings/recognizer_recording_timeout
        """

        if not request.get_json() or 'recognizer_recording_timeout' not in request.get_json():
            data = {
                "Error": "Wrong parameters, 'recognizer_recording_timeout' not set"
            }
            return jsonify(error=data), 400

        # get if present
        recognizer_recording_timeout = utils.get_value_flag_from_request(http_request=request,
                                                                         flag_to_find="recognizer_recording_timeout",
                                                                         is_boolean=False)

        SettingEditor.set_recognizer_recording_timeout(recognizer_recording_timeout=recognizer_recording_timeout)

        data = {
            "recognizer_recording_timeout": recognizer_recording_timeout
        }
        return jsonify(data), 200

    @requires_auth
    def get_recognizer_recording_timeout_with_silence(self):
        """
        Return the current recognizer_recording_timeout_with_silence value from settings

        Curl test
        curl -i --user admin:secret  -X GET  http://127.0.0.1:5000/settings/recognizer_recording_timeout_with_silence
        """

        if self.settings.options.recognizer_recording_timeout_with_silence is not None:
            data = {
                "recognizer_recording_timeout_with_silence": self.settings.options.recognizer_recording_timeout_with_silence
            }
            return jsonify(data), 200

        # if no Order instance
        data = {
            "error": "recognizer_recording_timeout_with_silence status not defined"
        }
        return jsonify(error=data), 400

    @requires_auth
    def set_recognizer_recording_timeout_with_silence(self):
        """
        Set the Kalliope Core recognizer_recording_timeout_with_silence value

        Curl test:
        curl -i -H "Content-Type: application/json" --user admin:secret  -X POST \
        -d '{"energy_threshold": "6666"}' http://127.0.0.1:5000/settings/recognizer_recording_timeout_with_silence
        """

        if not request.get_json() or 'recognizer_recording_timeout_with_silence' not in request.get_json():
            data = {
                "Error": "Wrong parameters, 'recognizer_recording_timeout_with_silence' not set"
            }
            return jsonify(error=data), 400

        # get if present
        recognizer_recording_timeout_with_silence = utils.get_value_flag_from_request(http_request=request,
                                                                                      flag_to_find="recognizer_recording_timeout_with_silence",
                                                                                      is_boolean=False)

        SettingEditor.set_recognizer_recording_timeout_with_silence(recognizer_recording_timeout_with_silence=recognizer_recording_timeout_with_silence)

        data = {
            "recognizer_recording_timeout_with_silence": recognizer_recording_timeout_with_silence
        }
        return jsonify(data), 200

    @requires_auth
    def get_default_tts(self):
        """
        Return the current default_tts value from settings

        Curl test
        curl -i --user admin:secret  -X GET  http://127.0.0.1:5000/settings/default_tts
        """

        # the default_tts settings
        if self.settings.default_tts_name is not None:
            data = {
                "default_tts": self.settings.default_tts_name
            }
            return jsonify(data), 200

        # if no Order instance
        data = {
            "error": "default_tts status not defined"
        }
        return jsonify(error=data), 400

    @requires_auth
    def set_default_tts(self):
        """
        Set the Kalliope Core default_tts value

        Curl test:
        curl -i -H "Content-Type: application/json" --user admin:secret  -X POST \
        -d '{"default_tts": "myTTS"}' http://127.0.0.1:5000/settings/default_tts
        """

        if not request.get_json() or 'default_tts' not in request.get_json():
            data = {
                "Error": "Wrong parameters, 'default_tts' not set"
            }
            return jsonify(error=data), 400

        # get if present
        value = utils.get_value_flag_from_request(http_request=request,
                                                  flag_to_find="default_tts",
                                                  is_boolean=False)

        SettingEditor.set_default_tts(default_tts_name=value)

        data = {
            "default_tts": self.settings.default_tts_name
        }
        return jsonify(data), 200

    @requires_auth
    def get_default_stt(self):
        """
        Return the current default_stt value from settings

        Curl test
        curl -i --user admin:secret  -X GET  http://127.0.0.1:5000/settings/default_stt
        """

        # the default_tts settings
        if self.settings.default_stt_name is not None:
            data = {
                "default_stt": self.settings.default_stt_name
            }
            return jsonify(data), 200

        # if no Order instance
        data = {
            "error": "default_stt status not defined"
        }
        return jsonify(error=data), 400

    @requires_auth
    def set_default_stt(self):
        """
        Set the Kalliope Core default_stt value

        Curl test:
        curl -i -H "Content-Type: application/json" --user admin:secret  -X POST \
        -d '{"default_stt": "myStt"}' http://127.0.0.1:5000/settings/default_stt
        """

        if not request.get_json() or 'default_stt' not in request.get_json():
            data = {
                "Error": "Wrong parameters, 'default_stt' not set"
            }
            return jsonify(error=data), 400

        # get if present
        value = utils.get_value_flag_from_request(http_request=request,
                                                  flag_to_find="default_stt",
                                                  is_boolean=False)

        SettingEditor.set_default_stt(default_stt_name=value)

        data = {
            "default_stt": self.settings.default_stt_name
        }
        return jsonify(data), 200

    @requires_auth
    def get_default_player(self):
        """
        Return the current default_player value from settings

        Curl test
        curl -i --user admin:secret  -X GET  http://127.0.0.1:5000/settings/default_player
        """

        # the default_player settings
        if self.settings.default_player_name is not None:
            data = {
                "default_player": self.settings.default_player_name
            }
            return jsonify(data), 200

        # if no Order instance
        data = {
            "error": "default_player status not defined"
        }
        return jsonify(error=data), 400

    @requires_auth
    def set_default_player(self):
        """
        Set the Kalliope Core default_player value

        Curl test:
        curl -i -H "Content-Type: application/json" --user admin:secret  -X POST \
        -d '{"default_player": "myPlayer"}' http://127.0.0.1:5000/settings/default_player
        """

        if not request.get_json() or 'default_player' not in request.get_json():
            data = {
                "Error": "Wrong parameters, 'default_player' not set"
            }
            return jsonify(error=data), 400
        # get if present
        value = utils.get_value_flag_from_request(http_request=request,
                                                  flag_to_find="default_player",
                                                  is_boolean=False)

        SettingEditor.set_default_player(default_player_name=value)

        data = {
            "default_player": self.settings.default_player_name
        }
        return jsonify(data), 200

    @requires_auth
    def get_default_trigger(self):
        """
        Return the current default_trigger value from settings

        Curl test
        curl -i --user admin:secret  -X GET  http://127.0.0.1:5000/settings/default_trigger
        """

        # the default_trigger settings
        if self.settings.default_trigger_name is not None:
            data = {
                "default_trigger": self.settings.default_trigger_name
            }
            return jsonify(data), 200

        # if no Order instance
        data = {
            "error": "default_trigger status not defined"
        }
        return jsonify(error=data), 400

    @requires_auth
    def set_default_trigger(self):
        """
        Set the Kalliope Core default_trigger value

        Curl test:
        curl -i -H "Content-Type: application/json" --user admin:secret  -X POST \
        -d '{"default_trigger": "myTrigger"}' http://127.0.0.1:5000/settings/default_trigger
        """

        if not request.get_json() or 'default_trigger' not in request.get_json():
            data = {
                "Error": "Wrong parameters, 'default_trigger' not set"
            }
            return jsonify(error=data), 400

        # get if present
        value = utils.get_value_flag_from_request(http_request=request,
                                                  flag_to_find="default_trigger",
                                                  is_boolean=False)

        SettingEditor.set_default_trigger(default_trigger=value)

        data = {
            "default_trigger": self.settings.default_trigger_name
        }
        return jsonify(data), 200

    @requires_auth
    def get_hooks(self):
        """
        Return the list of hooks from settings

        Curl test
        curl -i --user admin:secret  -X GET  http://127.0.0.1:5000/settings/hooks
        """

        if self.settings.hooks is not None:
            data = {
                "hooks": self.settings.hooks
            }
            return jsonify(data), 200

        # if no Order instance
        data = {
            "error": "hooks are not defined"
        }
        return jsonify(error=data), 400

    @requires_auth
    def set_hooks(self):
        """
        Set the Kalliope Core hooks value

        Curl test:
        curl -i -H "Content-Type: application/json" --user admin:secret  -X POST \
        -d '{"hook_name":"hook_value","hooke_name2":"hook_value2"}' http://127.0.0.1:5000/settings/hooks
        """

        if not request.get_json():
            data = {
                "Error": "No Parameters not"
            }
            return jsonify(error=data), 400

        # get if present
        value = request.get_json()

        if not isinstance(value, dict):
            data = {
                "Error": "Hooks must be a dictionary"
            }
            return jsonify(error=data), 400

        SettingEditor.set_hooks(hooks=value)

        data = {
            "hooks": self.settings.hooks
        }
        return jsonify(data), 200

    @requires_auth
    def get_variables(self):
        """
        Return the list of variables from settings

        Curl test
        curl -i --user admin:secret  -X GET  http://127.0.0.1:5000/settings/variables
        """

        if self.settings.variables is not None:
            data = {
                "variables": self.settings.variables
            }
            return jsonify(data), 200

        # if no Order instance
        data = {
            "error": "variables are not defined"
        }
        return jsonify(error=data), 400

    @requires_auth
    def set_variables(self):
        """
        Set the Kalliope Core variables value.
        Can be used with a dictionary of variables :
        curl -i -H "Content-Type: application/json" --user admin:secret  -X POST \
        -d '{"variable1":"variables_value","variables_name2":"variables_value2"}' http://127.0.0.1:5000/settings/varaibles
        """

        if not request.get_json():
            data = {
                "Error": "No Parameters provided"
            }
            return jsonify(error=data), 400

        # get if present
        value = request.get_json()

        if not isinstance(value, dict):
            data = {
                "Error": "Variables must be a dictionary"
            }
            return jsonify(error=data), 400

        SettingEditor.set_variables(variables=value)

        data = {
            "variables": self.settings.variables
        }
        return jsonify(data), 200

    def get_current_settings(self):
        """
        get the current settings config
        test with curl:
        curl -i --user admin:secret  -X GET  http://127.0.0.1:5000/settings
        """
        logger.debug("[FlaskAPI] get_current_settings: all")
        data = jsonify(settings=self.settings.serialize())
        return data, 200
