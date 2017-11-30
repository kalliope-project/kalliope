from kalliope.core.Utils.FileManager import FileManager
from requests.auth import HTTPBasicAuth
from kalliope.core.TTS.TTSModule import TTSModule
import logging
import requests


logging.basicConfig()
logger = logging.getLogger("kalliope")

TTS_URL = "https://stream.watsonplatform.net/text-to-speech/api/v1"
TTS_CONTENT_TYPE = "audio/wav"


class Watson(TTSModule):
    def __init__(self, **kwargs):
        super(Watson, self).__init__(**kwargs)

        # set parameter from what we receive from the settings
        self.username = kwargs.get('username', None)
        self.password = kwargs.get('password', None)
        self.voice = kwargs.get('voice', None)

    def say(self, words):
        """
        :param words: The sentence to say
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

        url = "%s/synthesize?voice=%s" % (TTS_URL, self.voice)

        response = requests.post(url,
                                 auth=HTTPBasicAuth(self.username, self.password),
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

