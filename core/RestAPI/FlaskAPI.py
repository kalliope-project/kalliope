import threading

from flask import jsonify

from core.ConfigurationManager.BrainLoader import BrainLoader
from core.RestAPI.utils import requires_auth
from core.SynapseLauncher import SynapseLauncher


class FlaskAPI(threading.Thread):
    def __init__(self, app, port=5000, brain_file=None):
        super(FlaskAPI, self).__init__()
        self.app = app
        self.port = port
        self.brain_file = brain_file
        self.brain_yaml = BrainLoader.get_yaml_config(file_path=self.brain_file)

        self.app.add_url_rule('/synapses/', view_func=self.get_synapses, methods=['GET'])
        self.app.add_url_rule('/synapses/<synapse_name>', view_func=self.get_synapse, methods=['GET'])
        self.app.add_url_rule('/synapses/<synapse_name>', view_func=self.run_synapse, methods=['POST'])

    def run(self):
        self.app.run(host='0.0.0.0', port="%s" % int(self.port), debug=True, threaded=True, use_reloader=False)

    def _get_synapse_by_name(self, synapse_name):
        """
        Find a synapse in the brain by its name
        :param synapse_name:
        :return:
        """
        all_synapse = self.brain_yaml
        for el in all_synapse:
            print el
            if el[0]["name"] in synapse_name:
                return el[0]
        return None

    @requires_auth
    def get_synapses(self):
        """
        get all synapse
        """
        data = jsonify(synapses=self.brain_yaml)
        return data, 200

    @requires_auth
    def get_synapse(self, synapse_name):
        """
        get a synapse by its name
        """
        synapse_target = self._get_synapse_by_name(synapse_name)
        if synapse_target is not None:
            data = jsonify(synapses=synapse_target)
            return data, 200

        data = {
            "synapse name not found": "%s" % synapse_name
        }
        return jsonify(error=data), 404

    @requires_auth
    def run_synapse(self, synapse_name):
        """
        Run a synapse by its name
        test with curl:
        curl -i --user admin:secret -X POST  http://localhost:5000/synapses/say-hello
        :param synapse_name:
        :return:
        """
        synapse_target = self._get_synapse_by_name(synapse_name)

        if synapse_target is None:
            data = {
                "synapse name not found": "%s" % synapse_name
            }
            return jsonify(error=data), 404

        # run the synapse
        SynapseLauncher.start_synapse(synapse_name, brain_file=self.brain_file)
        data = jsonify(synapses=synapse_target)
        return data, 201
