import subprocess
import os
from core import AudioPlayer

AUDIO_FREQUENCY = 16000
AUDIO_SIZE = -16
AUDIO_CHANNEL = 1
AUDIO_BUFFER = 2048


def say(words=None, language=None):
    temp_file = "/tmp/temp.wav"
    devnull = open("/dev/null", "w")
    subprocess.check_output(["/usr/bin/pico2wave", "-l=%s" % language, "-w=%s" % temp_file, words], stderr=devnull)
    AudioPlayer.play_audio(temp_file)
    devnull.close()

