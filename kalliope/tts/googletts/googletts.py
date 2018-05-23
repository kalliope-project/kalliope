import requests
from kalliope.core import FileManager
from kalliope.core.TTS.TTSModule import TTSModule, FailToLoadSoundFile, MissingTTSParameter
from pydub import AudioSegment
import logging

logging.basicConfig()
logger = logging.getLogger("kalliope")

TTS_URL = "http://translate.google.com/translate_tts"
TTS_CONTENT_TYPE = "audio/mpeg"
TTS_TIMEOUT_SEC = 30
MAX_REQUEST_LEN = 185
SENTENCE_SPLIT_DELIMITERS=['.', '!', '?', ';']


class Googletts(TTSModule):
    def __init__(self, **kwargs):
        super(Googletts, self).__init__(**kwargs)

        self._check_parameters()

    def say(self, words):
        """
        :param words: The sentence to say
        """

        self.generate_and_play(words, self._generate_audio_file)

    def _check_parameters(self):
        """
        Check parameters are ok, raise MissingTTSParameterException exception otherwise.
        :return: true if parameters are ok, raise an exception otherwise

               .. raises:: MissingTTSParameterException
        """
        if self.language == "default" or self.language is None:
            raise MissingTTSParameter("[GoogleTTS] Missing parameters, check documentation !")
        return True

    def _generate_audio_file(self):
        """
        Generic method used as a Callback in TTSModule
            - must provided the audio file and write it on the disk

        .. raises:: FailToLoadSoundFile
        """

        if (len(self.words) < 1):
            logger.error("Googletts : Invalid input %s", self.words)
            self.words = "I could not find an answer."

        # Prepare payload
        payloads = self.get_payloads()

        i = 0
        for payload in payloads:
            logger.debug(payload)
            # getting the audio
            r = requests.get(TTS_URL, params=payload, stream=True, timeout=TTS_TIMEOUT_SEC)
            content_type = r.headers['Content-Type']

            logger.debug("Googletts : Trying to get url: %s response code: %s and content-type: %s",
                     r.url,
                     r.status_code,
                     content_type)

            # Verify the response status code and the response content type
            if r.status_code != requests.codes.ok or content_type != TTS_CONTENT_TYPE:
                raise FailToLoadSoundFile("Googletts : Fail while trying to remotely access the audio file")

            # OK we get the audio we can write the sound file
            FileManager.write_in_file(self.file_path + str(i), r.content)
            i += 1

        # Stitch together all of the responses
        master_file = AudioSegment.from_mp3(self.file_path + "0")
        for x in range(1, i):
            master_file += AudioSegment.from_mp3(self.file_path + str(x))

        master_file.export(self.file_path, format="mp3")

    def get_payloads(self):
        """
        Generic method used load the payload used to access the remote api

        :return: Payload to use to access the remote api
        """
        qs = []
        logger.debug("Googletts : %s", self.words)
        if (self.split_sentences):
            logger.debug("Googletts : splitting sentences")
            request_text = ""
            for c in self.words:
                # If there is content in the request and we get to either the max or a delimiter, save the request
                if (len(request_text) > 0 and
                    c in SENTENCE_SPLIT_DELIMITERS or (len(request_text) >= MAX_REQUEST_LEN and c == ' ')):
                    qs.append({
                        "q": request_text + c,
                        "tl": self.language,
                        "ie": "UTF-8",
                        "total": "1",
                        "client": "tw-ob"
                        })
                    request_text = ""
                elif (c not in SENTENCE_SPLIT_DELIMITERS):
                    request_text += c

            # get the remainder if any
            if (len(request_text) > 0):
                qs.append({
                    "q": request_text,
                    "tl": self.language,
                    "ie": "UTF-8",
                    "total": "1",
                    "client": "tw-ob"
                    })
        else:
            logger.debug("Googletts : request may be too large for Google to handle, enable the split_sentences option if this becomes a problem.")
            qs.append({
                "q": self.words,
                "tl": self.language,
                "ie": "UTF-8",
                "total": "1",
                "client": "tw-ob"
                })

        return qs
