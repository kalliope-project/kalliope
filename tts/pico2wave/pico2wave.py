import subprocess
from core import AudioPlayer
from tts import TTS


class Pico2wave(TTS):

    def __init__(self, audio_player_type=None):
        TTS.__init__(self, audio_player_type)

    def say(self, words=None, language=None):
        temp_file = "/tmp/temp.wav"
        devnull = open("/dev/null", "w")
        subprocess.check_output(["/usr/bin/pico2wave", "-l=%s" % language, "-w=%s" % temp_file, words], stderr=devnull)
        self.play_audio(temp_file)
        devnull.close()

