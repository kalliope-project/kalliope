import logging
import os
import threading
import time

from flask import jsonify
from flask import request
from flask_cors import CORS
from flask_restful import abort
from werkzeug.utils import secure_filename

from kalliope.core.SignalLauncher import SignalLauncher
from kalliope._version import version_str
from kalliope.core.ConfigurationManager import SettingLoader, BrainLoader, SettingEditor
from kalliope.core.Lifo.LifoManager import LifoManager
from kalliope.core.Models.MatchedSynapse import MatchedSynapse
from kalliope.core.OrderListener import OrderListener
from kalliope.core.RestAPI.utils import requires_auth
from kalliope.core.SynapseLauncher import SynapseLauncher
from kalliope.core.Utils.FileManager import FileManager

logging.basicConfig()
logger = logging.getLogger("kalliope")

UPLOAD_FOLDER = '/tmp/kalliope/tmp_uploaded_audio'
ALLOWED_EXTENSIONS = {'mp3', 'wav'}


class FlaskAPI(threading.Thread):
    def __init__(self, app, port=5000, brain=None, allowed_cors_origin=False):
        """

        :param app: Flask API
        :param port: Port to listen
        :param brain: Brain object
        :type brain: Brain
        """
        super(FlaskAPI, self).__init__()
        self.app = app
        self.port = port
        self.brain = brain
        self.allowed_cors_origin = allowed_cors_origin

        # get current settings
        sl = SettingLoader()
        self.settings = sl.settings

        # api_response sent by the Order Analyser when using the /synapses/start/audio URL
        self.api_response = None
        # boolean used to notify the main process that we get the list of returned synapse
        self.order_analyser_return = False

        # configure the upload folder
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        # create the temp folder
        FileManager.create_directory(UPLOAD_FOLDER)

        # Flask configuration remove default Flask behaviour to encode to ASCII
        self.app.url_map.strict_slashes = False
        self.app.config['JSON_AS_ASCII'] = False

        if self.allowed_cors_origin is not False:
            CORS(app, resources={r"/*": {"origins": allowed_cors_origin}}, supports_credentials=True)

        # Add routing rules
        self.app.add_url_rule('/', view_func=self.get_main_page, methods=['GET'])
        self.app.add_url_rule('/synapses', view_func=self.get_synapses, methods=['GET'])
        self.app.add_url_rule('/synapses/<synapse_name>', view_func=self.get_synapse, methods=['GET'])
        self.app.add_url_rule('/synapses/start/id/<synapse_name>', view_func=self.run_synapse_by_name, methods=['POST'])
        self.app.add_url_rule('/synapses/start/order', view_func=self.run_synapse_by_order, methods=['POST'])
        self.app.add_url_rule('/synapses/start/audio', view_func=self.run_synapse_by_audio, methods=['POST'])
        self.app.add_url_rule('/shutdown/', view_func=self.shutdown_server, methods=['POST'])
        self.app.add_url_rule('/deaf/', view_func=self.get_deaf, methods=['GET'])
        self.app.add_url_rule('/deaf/', view_func=self.set_deaf, methods=['POST'])
        self.app.add_url_rule('/mute/', view_func=self.get_mute, methods=['GET'])
        self.app.add_url_rule('/mute/', view_func=self.set_mute, methods=['POST'])

    def run(self):
        self.app.run(host='0.0.0.0', port=int(self.port), debug=True, threaded=True, use_reloader=False)

    @requires_auth
    def get_main_page(self):
        logger.debug("[FlaskAPI] get_main_page")
        data = {
            "Kalliope version": "%s" % version_str
        }
        return jsonify(data), 200

    @staticmethod
    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def _get_synapse_by_name(self, synapse_name):
        """
        Find a synapse in the brain by its name
        :param synapse_name:
        :return:
        """
        all_synapse = self.brain.synapses
        for synapse in all_synapse:
            try:
                if synapse.name == synapse_name:
                    return synapse
            except KeyError:
                pass
        return None

    @requires_auth
    def get_synapses(self):
        """
        get all synapses.
        test with curl:
        curl -i --user admin:secret  -X GET  http://127.0.0.1:5000/synapses
        """
        logger.debug("[FlaskAPI] get_synapses: all")
        data = jsonify(synapses=[e.serialize() for e in self.brain.synapses])
        return data, 200

    @requires_auth
    def get_synapse(self, synapse_name):
        """
        get a synapse by its name
        test with curl:
        curl --user admin:secret -i -X GET  http://127.0.0.1:5000/synapses/say-hello-en
        """
        logger.debug("[FlaskAPI] get_synapse: synapse_name -> %s" % synapse_name)
        synapse_target = self._get_synapse_by_name(synapse_name)
        if synapse_target is not None:
            data = jsonify(synapses=synapse_target.serialize())
            return data, 200

        data = {
            "synapse name not found": "%s" % synapse_name
        }
        return jsonify(error=data), 404

    @requires_auth
    def run_synapse_by_name(self, synapse_name):
        """
        Run a synapse by its name
        test with curl:
        curl -i --user admin:secret -X POST  http://127.0.0.1:5000/synapses/start/id/say-hello-fr

        run a synapse without making kalliope speaking
        curl -i -H "Content-Type: application/json" --user admin:secret -X POST  \
        -d '{"mute":"true"}' http://127.0.0.1:5000/synapses/start/id/say-hello-fr

        Run a synapse by its name and pass order's parameters
        curl -i -H "Content-Type: application/json" --user admin:secret -X POST  \
        -d '{"mute":"true", "parameters": {"parameter1": "value1" }}' \
        http://127.0.0.1:5000/synapses/start/id/say-hello-fr

        :param synapse_name: name(id) of the synapse to execute
        :return:
        """
        # get a synapse object from the name
        logger.debug("[FlaskAPI] run_synapse_by_name: synapse name -> %s" % synapse_name)
        synapse_target = BrainLoader().brain.get_synapse_by_name(synapse_name=synapse_name)

        # Store the mute value, then apply depending of the request parameters
        old_mute_value = self.settings.options["mute"]
        mute = self.get_boolean_flag_from_request(request, boolean_flag_to_find="mute")
        if mute is not None:
            SettingEditor.set_mute_status(mute=mute)

        # get parameters
        parameters = self.get_parameters_from_request(request)

        if synapse_target is None:
            data = {
                "synapse name not found": "%s" % synapse_name
            }
            if mute is not None:
                SettingEditor.set_mute_status(mute=old_mute_value)
            return jsonify(error=data), 404
        else:
            # generate a MatchedSynapse from the synapse
            matched_synapse = MatchedSynapse(matched_synapse=synapse_target, overriding_parameter=parameters)
            # get the current LIFO buffer from the singleton
            lifo_buffer = LifoManager.get_singleton_lifo()
            lifo_buffer.add_synapse_list_to_lifo([matched_synapse])
            response = lifo_buffer.execute(is_api_call=True)
            data = jsonify(response)
            if mute is not None:
                SettingEditor.set_mute_status(mute=old_mute_value)
            return data, 201

    @requires_auth
    def run_synapse_by_order(self):
        """
        Give an order to Kalliope via API like it was from a spoken one
        Test with curl
        curl -i --user admin:secret -H "Content-Type: application/json" -X POST \
        -d '{"order":"my order"}' http://localhost:5000/synapses/start/order

        In case of quotes in the order or accents, use a file
        cat post.json:
        {"order":"j'aime"}
        curl -i --user admin:secret -H "Content-Type: application/json" -X POST \
        --data @post.json http://localhost:5000/order/

        Can be used with mute flag
        curl -i --user admin:secret -H "Content-Type: application/json" -X POST \
        -d '{"order":"my order", "mute":"true"}' http://localhost:5000/synapses/start/order

        :return:
        """
        if not request.get_json() or 'order' not in request.get_json():
            abort(400)

        order = request.get_json('order')

        # Store the mute value, then apply depending of the request parameters
        old_mute_value = self.settings.options["mute"]
        mute = self.get_boolean_flag_from_request(request, boolean_flag_to_find="mute")
        if mute is not None:
            SettingEditor.set_mute_status(mute=mute)

        if order is not None:
            # get the order
            order_to_run = order["order"]
            logger.debug("[FlaskAPI] run_synapse_by_order: order to run -> %s" % order_to_run)
            api_response = SynapseLauncher.run_matching_synapse_from_order(order_to_run,
                                                                           self.brain,
                                                                           self.settings,
                                                                           is_api_call=True)

            data = jsonify(api_response)
            if mute is not None:
                SettingEditor.set_mute_status(mute=old_mute_value)
            return data, 201
        else:
            data = {
                "error": "order cannot be null"
            }
            if mute is not None:
                SettingEditor.set_mute_status(mute=old_mute_value)
            return jsonify(error=data), 400

    @requires_auth
    def run_synapse_by_audio(self):
        """
        Give an order to Kalliope with an audio file
        Test with curl
        curl -i --user admin:secret -X POST  http://localhost:5000/synapses/start/audio -F "file=@/path/to/input.wav"

        With mute flag
        curl -i --user admin:secret -X POST http://localhost:5000/synapses/start/audio -F "file=@path/to/file.wav" -F mute="true"
        :return:
        """

        # check if the post request has the file part
        if 'file' not in request.files:
            data = {
                "error": "No file provided"
            }
            return jsonify(error=data), 400

        uploaded_file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if uploaded_file.filename == '':
            data = {
                "error": "No file provided"
            }
            return jsonify(error=data), 400

        # Store the mute value, then apply depending of the request parameters
        old_mute_value = self.settings.options["mute"]
        if request.form.get("mute"):
            SettingEditor.set_mute_status(mute=self.str_to_bool(request.form.get("mute")))

        # save the file
        filename = secure_filename(uploaded_file.filename)
        base_path = os.path.join(self.app.config['UPLOAD_FOLDER'])
        uploaded_file.save(os.path.join(base_path, filename))

        # now start analyse the audio with STT engine
        audio_path = base_path + os.sep + filename
        logger.debug("[FlaskAPI] run_synapse_by_audio: with file path %s" % audio_path)
        if not self.allowed_file(audio_path):
            audio_path = self._convert_to_wav(audio_file_path=audio_path)
        ol = OrderListener(callback=self.audio_analyser_callback, audio_file_path=audio_path)
        ol.start()
        ol.join()
        # wait the Order Analyser processing. We need to wait in this thread to keep the context
        while not self.order_analyser_return:
            time.sleep(0.1)
        self.order_analyser_return = False
        if self.api_response is not None and self.api_response:
            data = jsonify(self.api_response)
            self.api_response = None
            logger.debug("[FlaskAPI] run_synapse_by_audio: data %s" % data)
            if request.form.get("mute"):
                SettingEditor.set_mute_status(mute=old_mute_value)
            return data, 201
        else:
            data = {
                "error": "The given order doesn't match any synapses"
            }
            if request.form.get("mute"):
                SettingEditor.set_mute_status(mute=old_mute_value)
            return jsonify(error=data), 400

    @staticmethod
    def _convert_to_wav(audio_file_path):
        """
        If not already .wav, convert an incoming audio file to wav format. Using system avconv (raspberry)
        :param audio_file_path: the current full file path
        :return: Wave file path
        """
        # Not allowed so convert into wav using avconv (raspberry)
        base = os.path.splitext(audio_file_path)[0]
        extension = os.path.splitext(audio_file_path)[1]
        if extension != ".wav":
            current_file_path = audio_file_path
            audio_file_path = base + ".wav"
            os.system("avconv -y -i " + current_file_path + " " + audio_file_path)  # --> deprecated
            # subprocess.call(['avconv', '-y', '-i', audio_path, new_file_path], shell=True) # Not working ...

        return audio_file_path

    @requires_auth
    def shutdown_server(self):
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()
        return "Shutting down..."

    @requires_auth
    def get_deaf(self):
        """
        Return the current trigger status

        Curl test
        curl -i --user admin:secret  -X GET  http://127.0.0.1:5000/deaf
        """

        # find the order signal and call the deaf settings
        if self.settings.options["deaf"] is not None:
            data = {
                "deaf": self.settings.options["deaf"]
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
            abort(400)

        # get deaf if present
        deaf = self.get_boolean_flag_from_request(request, boolean_flag_to_find="deaf")

        signal_order = SignalLauncher.get_order_instance()
        if signal_order is not None and deaf is not None and self.settings.options["deaf"] is not None:
            SettingEditor.set_deaf_status(signal_order.trigger_instance, deaf)
            data = {
                "deaf": self.settings.options["deaf"]
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
        if self.settings.options["mute"] is not None:
            data = {
                "mute": self.settings.options["mute"]
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
            abort(400)

        # get mute if present
        mute = self.get_boolean_flag_from_request(request, boolean_flag_to_find="mute")
        SettingEditor.set_mute_status(mute=mute)

        data = {
            "mute": mute
        }
        return jsonify(data), 200

    def audio_analyser_callback(self, order):
        """
        Callback of the OrderListener. Called after the processing of the audio file
        This method will
        - call the Order Analyser to analyse the  order and launch corresponding synapse as usual.
        - get a list of launched synapse.
        - give the list to the main process via self.launched_synapses
        - notify that the processing is over via order_analyser_return
        :param order: string order to analyse
        :return:
        """
        logger.debug("[FlaskAPI] audio_analyser_callback: order to process -> %s" % order)
        api_response = SynapseLauncher.run_matching_synapse_from_order(order,
                                                                       self.brain,
                                                                       self.settings,
                                                                       is_api_call=True)
        self.api_response = api_response

        # this boolean will notify the main process that the order have been processed
        self.order_analyser_return = True

    def get_boolean_flag_from_request(self, http_request, boolean_flag_to_find):
        """
        Get the boolean flag from the request if exist, None otherwise !
        :param http_request:
        :param boolean_flag_to_find: json flag to find in the http_request
        :return: True or False if the boolean flag has been found in the request
        """
        boolean_flag = None
        try:
            received_json = http_request.get_json(force=True, silent=True, cache=True)
            if boolean_flag_to_find in received_json:
                boolean_flag = self.str_to_bool(received_json[boolean_flag_to_find])
        except TypeError:
            # no json received
            pass
        logger.debug("[FlaskAPI] Boolean %s : %s" % (boolean_flag_to_find, boolean_flag))
        return boolean_flag

    @staticmethod
    def str_to_bool(s):
        if isinstance(s, bool):  # do not convert if already a boolean
            return s
        else:
            if s == 'True' or s == 'true' or s == '1':
                return True
            elif s == 'False' or s == 'false' or s == '0':
                return False
            else:
                return False

    @staticmethod
    def get_parameters_from_request(http_request):
        """
        Get "parameters" object from the
        :param http_request:
        :return:
        """
        parameters = None
        try:
            received_json = http_request.get_json(silent=False, force=True)
            if 'parameters' in received_json:
                parameters = received_json['parameters']
        except TypeError:
            pass
        logger.debug("[FlaskAPI] Overridden parameters: %s" % parameters)

        return parameters
