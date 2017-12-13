import requests
from kalliope.core import FileManager
from kalliope.core.TTS.TTSModule import TTSModule, FailToLoadSoundFile, MissingTTSParameter
import logging
from voicerss_tts.voicerss_tts import TextToSpeech

logging.basicConfig()
logger = logging.getLogger("kalliope")

TTS_URL = "http://www.voicerss.org/controls/speech.ashx"
TTS_CONTENT_TYPE = "audio/mpeg"
TTS_TIMEOUT_SEC = 30


class Voicerss(TTSModule):
    def __init__(self, **kwargs):
        super(Voicerss, self).__init__(**kwargs)

        self.key = kwargs.get('key', None)
        self.rate = kwargs.get('rate', 0)
        self.codec = kwargs.get('codec', 'MP3')
        self.audio_format = kwargs.get('audio_format', '44khz_16bit_stereo')
        self.ssml = kwargs.get('ssml', False)
        self.base64 = kwargs.get('base64', False)
        self.ssl = kwargs.get('ssl', False)
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
        if self.language == "default" or self.language is None or self.key is None:
            raise MissingTTSParameter("[voicerss] Missing mandatory parameters, check documentation !")
        return True

    def _generate_audio_file(self):
        """
        Generic method used as a Callback in TTSModule
            - must provided the audio file and write it on the disk

        .. raises:: FailToLoadSoundFile
        """
        voicerss = TextToSpeech(
             api_key=self.key,
             text= self.words,
             language=self.language,
             rate=self.rate,
             codec=self.codec,
             audio_format=self.audio_format,
             ssml=self.ssml,
             base64=self.base64,
             ssl=self.ssl)

        # OK we get the audio we can write the sound file
        FileManager.write_in_file(self.file_path, voicerss.speech)
