import requests
from kalliope.core import FileManager
from kalliope.core.TTS.TTSModule import TTSModule, FailToLoadSoundFile
import logging

logging.basicConfig()
logger = logging.getLogger("kalliope")

TTS_URL = "http://www.voicerss.org/controls/speech.ashx"
TTS_CONTENT_TYPE = "audio/mpeg"
TTS_TIMEOUT_SEC = 30


class Voicerss(TTSModule):
    def __init__(self, **kwargs):
        super(Voicerss, self).__init__(**kwargs)

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
        # Prepare payload
        payload = self.get_payload()

        # getting the audio
        r = requests.get(TTS_URL, params=payload, stream=True, timeout=TTS_TIMEOUT_SEC)
        content_type = r.headers['Content-Type']

        logger.debug("Voicerss : Trying to get url: %s response code: %s and content-type: %s",
                     r.url,
                     r.status_code,
                     content_type)
        # Verify the response status code and the response content type
        if r.status_code != requests.codes.ok or content_type != TTS_CONTENT_TYPE:
            raise FailToLoadSoundFile("Voicerss : Fail while trying to remotely access the audio file")

        # OK we get the audio we can write the sound file
        FileManager.write_in_file(self.file_path, r.content)

    def get_payload(self):
        """
        Generic method used load the payload used to acces the remote api

        :return: Payload to use to access the remote api
        """

        return {
            "src": self.words,
            "hl": self.language,
            "c": "mp3"
        }
