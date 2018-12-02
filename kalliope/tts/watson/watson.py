from kalliope.core.Utils.FileManager import FileManager
from requests.auth import HTTPBasicAuth
from kalliope.core.TTS.TTSModule import TTSModule, MissingTTSParameter
import logging
import requests

logging.basicConfig()
logger = logging.getLogger("kalliope")

API_VERSION = "v1"
TTS_URL = "https://stream.watsonplatform.net/text-to-speech/api/"
TTS_CONTENT_TYPE = "audio/wav"


class Watson(TTSModule):
    def __init__(self, **kwargs):
        super(Watson, self).__init__(**kwargs)

        # set parameter from what we receive from the settings
        self.apikey = kwargs.get('apikey', None)
        self.location = kwargs.get('location', TTS_URL)
        self.voice = kwargs.get('voice', None)

        self._check_parameters()

    def _check_parameters(self):
        """
        Check parameters are ok, raise missingparameters exception otherwise.
        :return: true if parameters are ok, raise an exception otherwise

               .. raises:: MissingParameterException
        """
        if self.apikey is None or self.voice is None:
            raise MissingTTSParameter("[Watson] Missing parameters, check documentation !")
        return True

    def say(self, words):
        """
        """
        self.generate_and_play(words, self._generate_audio_file)

    def _generate_audio_file(self):
        """
        Generic method used as a Callback in TTSModule
        """

        # Prepare payload
        payload = self.get_payload()

        headers = {
            "Content-Type": "application/json",
            "Accept": "audio/wav"
        }

        endpoint_location = self.location if self.location.endswith('/') else self.location+"/"
        url = "%s/synthesize?voice=%s" % (endpoint_location + API_VERSION, self.voice)

        response = requests.post(url,
                                 auth=HTTPBasicAuth("apikey", self.apikey),
                                 headers=headers,
                                 json=payload)

        logger.debug("[Watson TTS] status code: %s" % response.status_code)

        if response.status_code == 200:
            # OK we get the audio we can write the sound file
            FileManager.write_in_file(self.file_path, response.content)
        else:
            logger.debug("[Watson TTS] Fail to get audio. Header: %s" % response.headers)

    def get_payload(self):
        return {
            "text": self.words
        }
