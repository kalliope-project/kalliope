import threading

from flask import jsonify

from core.ConfigurationManager.BrainLoader import BrainLoader
from core.RestAPI.utils import requires_auth


class FlaskAPI(threading.Thread):
    def __init__(self, app, brain):
        super(FlaskAPI, self).__init__()
        self.app = app
        self.brain = brain

        self.brain_yaml = BrainLoader.get_yaml_config()

        self.app.add_url_rule('/synapses', view_func=self.get_synapses, methods=['GET'])
        self.app.add_url_rule('/synapses/<synapse_name>', view_func=self.get_synapse, methods=['GET'])

    def run(self):
        self.app.run(host='0.0.0.0', debug=True, threaded=True, use_reloader=False)

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
        get all synapse
        """
        synapse_target = None
        all_synapse = self.brain_yaml
        for el in all_synapse:
            print el
            if el[0]["name"] in synapse_name:
                synapse_target = el[0]
        if synapse_target is not None:
            data = jsonify(synapses=synapse_target)
            return data, 200

        data = {
            "synapse name not found": "%s" % synapse_name
        }
        return jsonify(error=data), 404
