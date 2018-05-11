import requests

from kalliope.core import FileManager
from kalliope.core.TTS.TTSModule import TTSModule, FailToLoadSoundFile, MissingTTSParameter
import logging

logging.basicConfig()
logger = logging.getLogger("kalliope")



class Marytts(TTSModule):
    def __init__(self, **kwargs):
        super(Marytts, self).__init__(**kwargs)
        self.host = kwargs.get('host', 'localhost')
        self.port = kwargs.get('port', '59125')
        self.locale = kwargs.get('locale', None)
        self.voice = kwargs.get('voice', None)
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
        if self.locale is None or self.voice is None:
            raise MissingTTSParameter("[MaryTTS] Missing parameters, check documentation !")
        return True

    def _generate_audio_file(self):
        """
        Generic method used as a Callback in TTSModule
            - must provided the audio file and write it on the disk

        .. raises:: FailToLoadSoundFile
        """

        # Prepare payload
        payload = self.get_payload()

        # getting the audio
        r = requests.get('http://' + self.host + ':' + self.port + "/process?", payload)

        if r.status_code != 200:        
            raise FailToLoadSoundFile("MaryTTS : Fail while trying to remotely access the audio file")
        
        # OK we get the audio we can write the sound file
        FileManager.write_in_file(self.file_path, r.content)

    def get_payload(self):
        """
        Generic method used load the payload used to access the remote api

        :return: Payload to use to access the remote api
        """

        return {"INPUT_TEXT":self.words,
              "INPUT_TYPE":"TEXT",
              "LOCALE": self.locale,
              "VOICE":self.voice, 
              "OUTPUT_TYPE":"AUDIO",
              "AUDIO":"WAVE", 
              }