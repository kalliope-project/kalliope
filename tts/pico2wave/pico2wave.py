import os
import subprocess

from core.TTS.TTSModule import TTSModule
import logging
import sys

logging.basicConfig()
logger = logging.getLogger("kalliope")


class Pico2wave(TTSModule):

    def __init__(self, **kwargs):
        super(Pico2wave, self).__init__(**kwargs)

    def say(self, words):
        # the mother class TTSModule needs to know what we will generate to check the cache et generate the file path
        self.set_words(words)

        if not self.cache:
            # no cache, we need to generate the file
            self._generate_audio_file()
        else:
            # we check if the file already exist. If not we generate it with the TTS engine
            if not self.is_file_already_in_cache():
                self._generate_audio_file()

        # then play the generated audio file
        self.play_audio()

    def _generate_audio_file(self):
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

        # remove the extension .wav
        os.rename(tmp_path, self.file_path)


