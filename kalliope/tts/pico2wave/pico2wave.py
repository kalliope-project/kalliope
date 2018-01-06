import os
import subprocess

from kalliope.core.TTS.TTSModule import TTSModule, MissingTTSParameter
import sox

import logging
import sys

logging.basicConfig()
logger = logging.getLogger("kalliope")


class Pico2wave(TTSModule):

    def __init__(self, **kwargs):
        super(Pico2wave, self).__init__(**kwargs)
        self.samplerate = kwargs.get('samplerate', None)
        self.path = kwargs.get('path', None)

        self._check_parameters()

    def _check_parameters(self):
        """
        Check parameters are ok, raise MissingTTSParameters exception otherwise.
        :return: true if parameters are ok, raise an exception otherwise

               .. raises:: MissingTTSParameterException
        """
        if self.language == "default" or self.language is None:
            raise MissingTTSParameter("[pico2wave] Missing parameters, check documentation !")
        return True

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
        if self.path is None:
            # we try to get the path from the env
            self.path = self._get_pico_path()
            # if still None, we set a default value
            if self.path is None:
                self.path = "/usr/bin/pico2wave"

        # pico2wave needs that the file path ends with .wav
        tmp_path = self.file_path+".wav"
        pico2wave_options = ["-l=%s" % self.language, "-w=%s" % tmp_path]

        final_command = list()
        final_command.extend([self.path])
        final_command.extend(pico2wave_options)
        final_command.append(self.words)

        logger.debug("[Pico2wave] command: %s" % final_command)

        # generate the file with pico2wav
        subprocess.call(final_command)
        
        # convert samplerate
        if self.samplerate is not None:
            tfm = sox.Transformer()
            tfm.rate(samplerate=self.samplerate)
            tfm.build(str(tmp_path), str(tmp_path) + "tmp_name.wav")
            os.rename(str(tmp_path) + "tmp_name.wav", tmp_path)
        
        # remove the extension .wav
        os.rename(tmp_path, self.file_path)

    @staticmethod
    def _get_pico_path():
        prog = "pico2wave"
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, prog)
            if os.path.isfile(exe_file):
                return exe_file
        return None
