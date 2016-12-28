import threading

from flask import jsonify
from flask import request
from flask_restful import abort

from kalliope.core import OrderAnalyser
from kalliope.core.RestAPI.utils import requires_auth
from kalliope.core.SynapseLauncher import SynapseLauncher


class FlaskAPI(threading.Thread):
    def __init__(self, app, port=5000, brain=None):
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

        # Flask configuration remove default Flask behaviour to encode to ASCII
        self.app.url_map.strict_slashes = False
        self.app.config['JSON_AS_ASCII'] = False

        # Add routing rules
        self.app.add_url_rule('/synapses', view_func=self.get_synapses, methods=['GET'])
        self.app.add_url_rule('/synapses/<synapse_name>', view_func=self.get_synapse, methods=['GET'])
        self.app.add_url_rule('/synapses/<synapse_name>', view_func=self.run_synapse, methods=['POST'])
        self.app.add_url_rule('/order/', view_func=self.run_order, methods=['POST'])
        self.app.add_url_rule('/shutdown/', view_func=self.shutdown_server, methods=['POST'])


    def run(self):
        self.app.run(host='0.0.0.0', port="%s" % int(self.port), debug=True, threaded=True, use_reloader=False)

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
        """
        data = jsonify(synapses=[e.serialize() for e in self.brain.synapses])
        return data, 200

    @requires_auth
    def get_synapse(self, synapse_name):
        """
        get a synapse by its name
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
        SynapseLauncher.start_synapse(synapse_name, brain=self.brain)
        data = jsonify(synapses=synapse_target)
        return data, 201

    @requires_auth
    def run_order(self):
        """
        Give an order to Kalliope via API like it was from a spoken one
        Test with curl
        curl -i --user admin:secret -H "Content-Type: application/json" -X POST -d '{"order":"my order"}' http://localhost:5000/order
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
            oa = OrderAnalyser(order=order_to_run, brain=self.brain)
            launched_synapses = oa.start()

            if launched_synapses:
                # if the list is not empty, we have launched one or more synapses
                data = jsonify(synapses=[e.serialize() for e in launched_synapses])
                return data, 201
            else:
                data = {
                    "error": "The given order doesn't match any synapses"
                }
                return jsonify(error=data), 400

        else:
            data = {
                "error": "order cannot be null"
            }
            return jsonify(error=data), 400

    @requires_auth
    def shutdown_server(self):
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()
        return "Shutting down..."
