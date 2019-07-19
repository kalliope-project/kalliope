import logging
import threading

from flask import jsonify
from flask import request
from flask_cors import CORS

from kalliope._version import version_str
from kalliope.core.ConfigurationManager import SettingLoader
from kalliope.core.RestAPI.utils import requires_auth
from kalliope.core.RestAPI.views.settings_views import SettingsView
from kalliope.core.RestAPI.views.synapses_views import SynapsesView
from kalliope.core.Utils.FileManager import FileManager

logging.basicConfig()
logger = logging.getLogger("kalliope")

UPLOAD_FOLDER = '/tmp/kalliope/tmp_uploaded_audio'
ALLOWED_EXTENSIONS = {'wav'}


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
        self.app.add_url_rule('/shutdown/', view_func=self.shutdown_server, methods=['POST'])

        # Register blue prints
        self.synapses_blueprint = SynapsesView('synapses', __name__, app=self.app, brain=self.brain, settings=self.settings)
        self.app.register_blueprint(self.synapses_blueprint)
        self.settings_blueprint = SettingsView('settings', __name__, app=self.app, brain=self.brain, settings=self.settings)
        self.app.register_blueprint(self.settings_blueprint)

    def run(self):
        self.app.run(host='0.0.0.0', port=int(self.port), debug=True, threaded=True, use_reloader=False)

    @requires_auth
    def get_main_page(self):
        logger.debug("[FlaskAPI] get_main_page")
        data = {
            "Kalliope version": "%s" % version_str
        }
        return jsonify(data), 200

    @requires_auth
    def shutdown_server(self):
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()
        return "Shutting down..."
