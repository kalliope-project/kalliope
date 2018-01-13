from kalliope.core.TTS.TTSModule import TTSModule, MissingTTSParameter
import logging
import sys
import subprocess

logging.basicConfig()
logger = logging.getLogger("kalliope")


class Espeak(TTSModule):

    def __init__(self, **kwargs):
        super(Espeak, self).__init__(language="any", **kwargs)

        # set parameter from what we receive from the settings
        self.variant = kwargs.get('variant', None)
        self.speed = str(kwargs.get('speed', '160'))
        self.amplitude = str(kwargs.get('amplitude', '100'))
        self.pitch = str(kwargs.get('pitch', '50'))
        self.espeak_exec_path = kwargs.get('path', r'/usr/bin/espeak')

        if self.voice == 'default' or self.voice is None:
            raise MissingTTSParameter("voice parameter is required by the eSpeak TTS")

        # if voice = default, don't add voice option to espeak
        if self.variant is None:
            self.voice_and_variant = self.voice
        else:
            self.voice_and_variant = self.voice + '+' + self.variant

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

        options = {
            'v': '-v' + self.voice_and_variant,
            's': '-s' + self.speed,
            'a': '-a' + self.amplitude,
            'p': '-p' + self.pitch,
            'w': '-w' + self.file_path
        }

        final_command = [self.espeak_exec_path, options['v'], options['s'], options['a'],
                         options['p'], options['w'], self.words]

        # generate the file with eSpeak
        subprocess.call(final_command, stderr=sys.stderr)
