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
        self.add_url_rule('/settings/ambient_noise_second/', view_func=self.get_ambient_noise_second,
                          methods=['GET'])
        self.add_url_rule('/settings/ambient_noise_second/', view_func=self.set_adjust_for_ambient_noise_second,
                          methods=['POST'])
        self.add_url_rule('/settings/energy_threshold/', view_func=self.get_energy_threshold,
                          methods=['GET'])
        self.add_url_rule('/settings/energy_threshold/', view_func=self.set_energy_threshold,
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
    def get_energy_threshold(self):
        """
        Return the current energy_threshold value from settings

        Curl test
        curl -i --user admin:secret  -X GET  http://127.0.0.1:5000/settings/energy_threshold
        """

        if self.settings.options.energy_threshold is not None:
            data = {
                "energy_threshold": self.settings.options.energy_threshold
            }
            return jsonify(data), 200

        # if no Order instance
        data = {
            "error": "energy_threshold status not defined"
        }
        return jsonify(error=data), 400

    @requires_auth
    def set_energy_threshold(self):
        """
        Set the Kalliope Core energy_threshold value

        Curl test:
        curl -i -H "Content-Type: application/json" --user admin:secret  -X POST \
        -d '{"energy_threshold": "6666"}' http://127.0.0.1:5000/settings/energy_threshold
        """

        if not request.get_json() or 'energy_threshold' not in request.get_json():
            data = {
                "Error": "Wrong parameters, 'energy_threshold' not set"
            }
            return jsonify(error=data), 400

        # get energy_threshold if present
        energy_threshold = utils.get_value_flag_from_request(http_request=request,
                                                             flag_to_find="energy_threshold",
                                                             is_boolean=False)

        SettingEditor.set_energy_threshold(energy_threshold=energy_threshold)

        data = {
            "energy_threshold": energy_threshold
        }
        return jsonify(data), 200

    @requires_auth
    def get_ambient_noise_second(self):
        """
        Return the current ambient_noise_second value from settings

        Curl test
        curl -i --user admin:secret  -X GET  http://127.0.0.1:5000/settings/ambient_noise_second
        """

        if self.settings.options.adjust_for_ambient_noise_second is not None:
            data = {
                "ambient_noise_second": self.settings.options.adjust_for_ambient_noise_second
            }
            return jsonify(data), 200

        # if no Order instance
        data = {
            "error": "ambient_noise_second status not defined"
        }
        return jsonify(error=data), 400

    @requires_auth
    def set_adjust_for_ambient_noise_second(self):
        """
        Set the Kalliope Core ambient_noise_second value

        Curl test:
        curl -i -H "Content-Type: application/json" --user admin:secret  -X POST \
        -d '{"energy_threshold": "6666"}' http://127.0.0.1:5000/settings/ambient_noise_second
        """

        if not request.get_json() or 'ambient_noise_second' not in request.get_json():
            data = {
                "Error": "Wrong parameters, 'ambient_noise_second' not set"
            }
            return jsonify(error=data), 400

        # get if present
        ambient_noise_second = utils.get_value_flag_from_request(http_request=request,
                                                                 flag_to_find="ambient_noise_second",
                                                                 is_boolean=False)

        SettingEditor.set_adjust_for_ambient_noise_second(adjust_for_ambient_noise_second=ambient_noise_second)

        data = {
            "ambient_noise_second": ambient_noise_second
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
