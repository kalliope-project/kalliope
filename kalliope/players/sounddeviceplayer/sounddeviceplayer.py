# -*- coding: utf-8 -*-
import sounddevice as sd
import soundfile as sf
import logging

logging.basicConfig()
logger = logging.getLogger("kalliope")

FS = 48000


class Sounddeviceplayer(object):
    """
    This Class is representing the Player Object used to play the all sound of the system.
    """

    def __init__(self, **kwargs):
        logger.debug("[Sounddeviceplayer.__init__] instance")
        logger.debug("[Sounddeviceplayer.__init__] args : %s " % str(kwargs))

    @classmethod
    def play(cls, file_path):

        data, fs = sf.read(file_path)
        sd.play(data, fs)
        sd.wait()
