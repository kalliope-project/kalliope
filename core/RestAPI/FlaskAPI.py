import threading

from flask import jsonify

from core.ConfigurationManager.BrainLoader import BrainLoader
from core.RestAPI.utils import requires_auth


class FlaskAPI(threading.Thread):
    def __init__(self, app, brain):
        super(FlaskAPI, self).__init__()
        self.app = app
        self.brain = brain

        self.app.add_url_rule('/synapses', view_func=self.get_synapses, methods=['GET'])

    def run(self):
        self.app.run(host='0.0.0.0', debug=True, threaded=True, use_reloader=False)

    @requires_auth
    def get_synapses(self):
        """
        get all synapse
        """
        data = jsonify(synapses=BrainLoader.get_yaml_config())
        return data, 200
