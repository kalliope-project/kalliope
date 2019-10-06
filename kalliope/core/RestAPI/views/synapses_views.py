import logging
import os
import time

from flask import jsonify, Blueprint
from flask import request
from werkzeug.utils import secure_filename

from kalliope import Utils
from kalliope.core.ConfigurationManager import BrainLoader, SettingEditor
from kalliope.core.ConfigurationManager.ConfigurationChecker import KalliopeModuleNotFoundError, ConfigurationChecker, \
    InvalidSynapeName, NoSynapeNeurons, NoSynapeSignals
from kalliope.core.Cortex import Cortex
from kalliope.core.Lifo.LifoManager import LifoManager
from kalliope.core.Models import Synapse
from kalliope.core.Models.MatchedSynapse import MatchedSynapse
from kalliope.core.OrderListener import OrderListener
from kalliope.core.RestAPI import utils
from kalliope.core.RestAPI.utils import requires_auth
from kalliope.core.SynapseLauncher import SynapseLauncher

logging.basicConfig()
logger = logging.getLogger("kalliope")

UPLOAD_FOLDER = '/tmp/kalliope/tmp_uploaded_audio'
ALLOWED_EXTENSIONS = {'wav'}


class SynapsesView(Blueprint):
    def __init__(self, name, import_name, app, brain=None, settings=None):
        self.brain = brain
        self.settings = settings
        self.app = app
        super().__init__(name, import_name)

        # api_response sent by the Order Analyser when using the /synapses/start/audio URL
        self.api_response = None
        # boolean used to notify the main process that we get the list of returned synapse
        self.order_analyser_return = False

        # routes
        self.add_url_rule('/synapses', view_func=self.get_synapses, methods=['GET'])
        self.add_url_rule('/synapses', view_func=self.create_synapses, methods=['POST'])
        self.add_url_rule('/synapses/<synapse_name>', view_func=self.get_synapse, methods=['GET'])
        self.add_url_rule('/synapses/<synapse_name>', view_func=self.delete_synapse, methods=['DELETE'])
        self.add_url_rule('/synapses/start/id/<synapse_name>', view_func=self.run_synapse_by_name, methods=['POST'])
        self.add_url_rule('/synapses/start/order', view_func=self.run_synapse_by_order, methods=['POST'])
        self.add_url_rule('/synapses/start/audio', view_func=self.run_synapse_by_audio, methods=['POST'])

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
    def create_synapses(self):
        """
        curl -i -H "Content-Type: application/json" \
        --user admin:secret \
        -X POST \
        -d '{
          "name": "Say-hello",
          "signals": [
            {
              "order": "je suis nicolas"
            }
          ],
          "neurons": [
            {
              "say": {
                "message": "je sais"
              }
            }
          ]
        }' \
        http://127.0.0.1:5000/synapses
        :return:
        """
        if not request.get_json() or 'name' not in request.get_json():
            data = {
                "Error": "Wrong parameters, 'name' not set"
            }
            return jsonify(error=data), 400

        new_synapse = request.get_json()
        try:
            ConfigurationChecker().check_synape_dict(new_synapse)
        except (InvalidSynapeName, NoSynapeNeurons, NoSynapeSignals) as e:
            data = {
                "error": "%s" % e
            }
            return jsonify(data), 400

        try:
            name = new_synapse["name"]
            neurons = BrainLoader.get_neurons(new_synapse["neurons"], self.settings)
            signals = BrainLoader.get_signals(new_synapse["signals"])
            new_synapse_instance = Synapse(name=name, neurons=neurons, signals=signals)
            self.brain.synapses.append(new_synapse_instance)
            # TODO save the brain in yaml
            return jsonify(new_synapse_instance.serialize()), 201
        except KalliopeModuleNotFoundError as e:
            data = {
                "error": "%s" % e
            }
            return jsonify(data), 400

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
    def delete_synapse(self, synapse_name):
        """
        delete a synapse by its name
        test with curl:
        curl --user admin:secret -i -X DELETE  http://127.0.0.1:5000/synapses/say-hello-en
        """
        logger.debug("[FlaskAPI] delete_synapse -> %s" % synapse_name)
        synapse_target = self._get_synapse_by_name(synapse_name)
        if synapse_target is not None:
            # delete from brain
            self._delete_synapse_by_name(synapse_name)
            return '', 204

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
        old_mute_value = self.settings.options.mute
        mute = utils.get_value_flag_from_request(http_request=request,
                                                 flag_to_find="mute",
                                                 is_boolean=True)
        if mute is not None:
            SettingEditor.set_mute_status(mute=mute)

        # get parameters
        parameters = utils.get_parameters_from_request(request)

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
            data = {
                "Error": "Wrong parameters, 'order' not set"
            }
            return jsonify(error=data), 400

        order = request.get_json('order')

        # Store the mute value, then apply depending of the request parameters
        old_mute_value = self.settings.options.mute
        mute = utils.get_value_flag_from_request(http_request=request,
                                                 flag_to_find="mute",
                                                 is_boolean=True)
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

            Cortex.save('kalliope_last_order', order_to_run)
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
        curl -i --user admin:secret -X POST \
        http://localhost:5000/synapses/start/audio -F "file=@path/to/file.wav" -F mute="true"
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
        old_mute_value = self.settings.options.mute
        if request.form.get("mute"):
            SettingEditor.set_mute_status(mute=Utils.str_to_bool(request.form.get("mute")))

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
        Cortex.save('kalliope_last_order', order)
        # this boolean will notify the main process that the order have been processed
        self.order_analyser_return = True

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
            logger.debug("Converting file " + current_file_path + " to .wav")
            audio_file_path = base + ".wav"
            os.system("ffmpeg -loglevel panic -y -i " + current_file_path + " " + audio_file_path)  # --> deprecated
            # subprocess.call(['avconv', '-y', '-i', audio_path, new_file_path], shell=True) # Not working ...

        return audio_file_path

    @staticmethod
    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def _delete_synapse_by_name(self, synapse_name):
        all_synapse = self.brain.synapses
        for synapse in all_synapse:
            try:
                if synapse.name == synapse_name:
                    logger.debug("[FlaskAPI] remove synapse from the brain: '%s'" % synapse_name)
                    all_synapse.remove(synapse)
                    # TODO save the brain in yaml
            except KeyError:
                pass
        return None
