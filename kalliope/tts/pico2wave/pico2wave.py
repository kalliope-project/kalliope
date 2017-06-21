import os
import subprocess

from kalliope.core.TTS.TTSModule import TTSModule
import logging
import sys

logging.basicConfig()
logger = logging.getLogger("kalliope")


class Pico2wave(TTSModule):

    def __init__(self, **kwargs):
        super(Pico2wave, self).__init__(**kwargs)

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

        pico2wave_exec_path = ["/usr/bin/pico2wave"]

        # pico2wave needs that the file path ends with .wav
        tmp_path = self.file_path+".wav"
        pico2wave_options = ["-l=%s" % self.language, "-w=%s" % tmp_path]

        final_command = list()
        final_command.extend(pico2wave_exec_path)
        final_command.extend(pico2wave_options)
        final_command.append(self.words)

        logger.debug("Pico2wave command: %s" % final_command)

        # generate the file with pico2wav
        subprocess.call(final_command, stderr=sys.stderr)
        
        # change samplerate from 16.000 hz to 44.100 hz
        if self.change_rate is True:
            tfm = sox.Transformer()
            tfm.rate(samplerate=44100)
            tfm.build(str(tmp_path), str(tmp_path)+("tmp_name.wav"))
            os.rename(str(tmp_path)+("tmp_name.wav"), tmp_path)
        
        # remove the extension .wav
        os.rename(tmp_path, self.file_path)
