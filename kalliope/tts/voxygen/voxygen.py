import logging

import requests

from kalliope.core import FileManager
from kalliope.core.TTS.TTSModule import TTSModule, MissingTTSParameter

logging.basicConfig()
logger = logging.getLogger("kalliope")

TTS_URL = "https://www.voxygen.fr/sites/all/modules/voxygen_voices/assets/proxy/index.php"
TTS_TIMEOUT_SEC = 30
TTS_CONTENT_TYPE = "audio/mpeg"


class Voxygen(TTSModule):

    def __init__(self, **kwargs):
        # voxygen does'nt need a language. The name of the voice correspond to a lang
        super(Voxygen, self).__init__(language="any", **kwargs)

        self.voice = kwargs.get('voice', None)
        if self.voice is None:
            raise MissingTTSParameter("voice parameter is required by the Voxygen TTS")

    def say(self, words):
        """
        :param words: The sentence to say
        """

        self.generate_and_play(words, self._generate_audio_file)

    def _generate_audio_file(self):
        """
        Generic method used as a Callback in TTSModule
            - must provided the audio file and write it on the disk

        .. raises:: FailToLoadSoundFile
        """

        payload = self.get_payload(self.voice, self.words)

        # getting the mp3
        r = requests.get(TTS_URL, params=payload, stream=True, timeout=TTS_TIMEOUT_SEC)
        content_type = r.headers['Content-Type']

        logger.debug("Voxygen : Trying to get url: %s response code: %s and content-type: %s",
                     r.url,
                     r.status_code,
                     content_type)

        if r.status_code == requests.codes.ok and content_type == TTS_CONTENT_TYPE:
            FileManager.write_in_file(self.file_path, r.content)
        else:
            logger.debug("Unable to get a valid audio file. Returned code: %s" % r.status_code)

    @staticmethod
    def get_payload(voice, words):
        """
        Generic method used load the payload used to access the remote api

        :return: Payload to use to access the remote api
        """

        return {
            "method": "redirect",
            "text": words,
            "voice": voice
        }
