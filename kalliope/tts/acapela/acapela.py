import logging
import re

import requests

from kalliope.core import FileManager
from kalliope.core.TTS.TTSModule import TTSModule, FailToLoadSoundFile, MissingTTSParameter

logging.basicConfig()
logger = logging.getLogger("kalliope")

TTS_URL = "https://acapela-box.com/AcaBox/dovaas.php"
TTS_CONTENT_TYPE = "audio/mpeg"
TTS_TIMEOUT_SEC = 30


class TCPTimeOutError(Exception):
    """
    This error is raised when the TCP connection has been lost. Probably due to a low internet
    connection while trying to access the remote API.
    """
    pass


class Acapela(TTSModule):
    def __init__(self, **kwargs):
        super(Acapela, self).__init__(**kwargs)

        self.voice = kwargs.get('voice', None)
        if self.voice is None:
            raise MissingTTSParameter("voice parameter is required by the Acapela TTS")

        # speech rate
        self.spd = kwargs.get('spd', 180)
        # VOICE SHAPING
        self.vct = kwargs.get('vct', 100)

        self.words = None

    def say(self, words):
        """
        :param words: The sentence to say
        """
        self.words = words
        self.generate_and_play(words, self._generate_audio_file)

    def _generate_audio_file(self):
        """
        Generic method used as a Callback in TTSModule
            - must provided the audio file and write it on the disk

        .. raises:: FailToLoadSoundFile, TCPTimeOutError
        """
        # Prepare payload
        payload = self.get_payload()

        cookie = Acapela._get_cookie()

        # Get the mp3 URL from the page
        mp3_url = Acapela.get_audio_link(TTS_URL, payload, cookie)

        # getting the mp3
        headers = {
            "Cookie": "%s" % cookie
        }
        r = requests.get(mp3_url, headers=headers, stream=True, timeout=TTS_TIMEOUT_SEC)
        content_type = r.headers['Content-Type']

        logger.debug("Acapela : Trying to get url: %s response code: %s and content-type: %s",
                     r.url,
                     r.status_code,
                     content_type)
        # Verify the response status code and the response content type
        if r.status_code != requests.codes.ok or content_type != TTS_CONTENT_TYPE:
            raise FailToLoadSoundFile("Acapela : Fail while trying to remotely access the audio file")

        # OK we get the audio we can write the sound file
        FileManager.write_in_file(self.file_path, r.content)

    def get_payload(self):
        """
        Generic method used load the payload used to access the remote api
        :return: Payload to use to access the remote api
        """
        return {
            "text": "%s" % self.words,
            "voice": "%s22k" % self.voice,
            "spd": "%s" % self.spd,
            "vct": "%s" % self.vct,
            "codecMP3": "1",
            "format": "WAV 22kHz",
            "listen": 1
        }

    @staticmethod
    def get_audio_link(url, payload, cookie, timeout_expected=TTS_TIMEOUT_SEC):
        """
        Return the audio link

        :param url: the url to access
        :param payload: the payload to use to access the remote api
        :param timeout_expected: timeout before the post request is cancel
        :param cookie: cookie used for authentication
        :return: the audio link
        :rtype: String
        """
        headers = {
            "Cookie": "%s" % cookie
        }

        r = requests.post(url, data=payload, headers=headers, timeout=timeout_expected)
        data = r.json()
        return data["snd_url"]

    @staticmethod
    def _get_cookie():
        """
        Get a cookie that is used to authenticate post request
        :return: the str cookie
        """
        returned_cookie = ""
        index_url = "https://acapela-box.com/AcaBox/index.php"
        r = requests.get(index_url)

        regex = "(acabox=\w+)"
        cookie_match = re.match(regex, r.headers["Set-Cookie"])

        if cookie_match:
            returned_cookie = cookie_match.group(1)

        return returned_cookie
