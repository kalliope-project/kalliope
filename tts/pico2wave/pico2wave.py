import subprocess
import os


def say(words):
    tempfile = "temp.wav"
    devnull = open("/dev/null", "w")
    subprocess.call(["pico2wave", "-l=fr-FR", "-w", tempfile, words], stderr=devnull)
    subprocess.call(["aplay", tempfile], stderr=devnull)
    os.remove(tempfile)
