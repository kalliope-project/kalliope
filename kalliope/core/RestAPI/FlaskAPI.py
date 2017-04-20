import logging
import os
import threading

import time

from kalliope.core.LIFOBuffer import LIFOBuffer
from kalliope.core.Models.MatchedSynapse import MatchedSynapse
from kalliope.core.Utils.FileManager import FileManager

from kalliope.core.ConfigurationManager import SettingLoader, BrainLoader
from kalliope.core.OrderListener import OrderListener
from werkzeug.utils import secure_filename

from flask import jsonify
from flask import request
from flask_restful import abort
from flask_cors import CORS

from kalliope.core.RestAPI.utils import requires_auth
from kalliope.core.SynapseLauncher import SynapseLauncher
from kalliope._version import version_str

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
            cors = CORS(app, resources={r"/*": {"origins": allowed_cors_origin}}, supports_credentials=True)

        # Add routing rules
        self.app.add_url_rule('/', view_func=self.get_main_page, methods=['GET'])
        self.app.add_url_rule('/synapses', view_func=self.get_synapses, methods=['GET'])
        self.app.add_url_rule('/synapses/<synapse_name>', view_func=self.get_synapse, methods=['GET'])
        self.app.add_url_rule('/synapses/start/id/<synapse_name>', view_func=self.run_synapse_by_name, methods=['POST'])
        self.app.add_url_rule('/synapses/start/order', view_func=self.run_synapse_by_order, methods=['POST'])
        self.app.add_url_rule('/synapses/start/audio', view_func=self.run_synapse_by_audio, methods=['POST'])
        self.app.add_url_rule('/shutdown/', view_func=self.shutdown_server, methods=['POST'])

    def run(self):
        self.app.run(host='0.0.0.0', port="%s" % int(self.port), debug=True, threaded=True, use_reloader=False)

    def get_main_page(self):
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
        data = jsonify(synapses=[e.serialize() for e in self.brain.synapses])
        return data, 200

    @requires_auth
    def get_synapse(self, synapse_name):
        """
        get a synapse by its name
        test with curl:
        curl --user admin:secret -i -X GET  http://127.0.0.1:5000/synapses/say-hello-en
        """
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
        :param synapse_name:
        :return:
        """
        # get a synapse object from the name
        synapse_target = BrainLoader().get_brain().get_synapse_by_name(synapse_name=synapse_name)

        if synapse_target is None:
            data = {
                "synapse name not found": "%s" % synapse_name
            }
            return jsonify(error=data), 404
        else:
            # generate a MatchedSynapse from the synapse
            matched_synapse = MatchedSynapse(matched_synapse=synapse_target)
            # get the current LIFO buffer
            lifo_buffer = LIFOBuffer()
            # this is a new call we clean up the LIFO
            lifo_buffer.clean()
            lifo_buffer.add_synapse_list_to_lifo([matched_synapse])
            response = lifo_buffer.execute(is_api_call=True)
            data = jsonify(response)
            return data, 201

    @requires_auth
    def run_synapse_by_order(self):
        """
        Give an order to Kalliope via API like it was from a spoken one
        Test with curl
        curl -i --user admin:secret -H "Content-Type: application/json" -X POST -d '{"order":"my order"}' http://localhost:5000/synapses/start/order
        In case of quotes in the order or accents, use a file
        cat post.json:
        {"order":"j'aime"}
        curl -i --user admin:secret -H "Content-Type: application/json" -X POST --data @post.json http://localhost:5000/order/
        :return:
        """
        if not request.get_json() or 'order' not in request.get_json():
            abort(400)

        order = request.get_json('order')
        if order is not None:
            # get the order
            order_to_run = order["order"]

            api_response = SynapseLauncher.run_matching_synapse_from_order(order_to_run,
                                                                           self.brain,
                                                                           self.settings,
                                                                           is_api_call=True)

            data = jsonify(api_response)
            return data, 201
        else:
            data = {
                "error": "order cannot be null"
            }
            return jsonify(error=data), 400

    def run_synapse_by_audio(self):
        """
        Give an order to Kalliope with an audio file
        Test with curl
        curl -i --user admin:secret -X POST  http://localhost:5000/synapses/start/audio -F "file=@/path/to/input.wav"
        :return:
        """
        # check if the post request has the file part
        if 'file' not in request.files:
            data = {
                "error": "No file provided"
            }
            return jsonify(error=data), 400

        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            data = {
                "error": "No file provided"
            }
            return jsonify(error=data), 400
        if file and self.allowed_file(file.filename):
            # save the file
            filename = secure_filename(file.filename)
            base_path = os.path.join(self.app.config['UPLOAD_FOLDER'])
            file.save(os.path.join(base_path, filename))

            # now start analyse the audio with STT engine
            audio_path = base_path + os.sep + filename
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
                return data, 201
            else:
                data = {
                    "error": "The given order doesn't match any synapses"
                }
                return jsonify(error=data), 400

    @requires_auth
    def shutdown_server(self):
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()
        return "Shutting down..."

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
        logger.debug("order to process %s" % order)
        api_response = SynapseLauncher.run_matching_synapse_from_order(order,
                                                                       self.brain,
                                                                       self.settings,
                                                                       is_api_call=True)
        self.api_response = api_response

        # this boolean will notify the main process that the order have been processed
        self.order_analyser_return = True
