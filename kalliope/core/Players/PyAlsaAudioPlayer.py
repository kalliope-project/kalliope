# -*- coding: utf-8 -*-
import alsaaudio
import logging
import wave

logging.basicConfig()
logger = logging.getLogger("kalliope")


class PyAlsaAudioPlayer(object):
    """
    This Class is representing the Player Object used to play the all sound of the system.
    """

    def __init__(self):
        pass

    @classmethod
    def play(cls, file_path):

        f = wave.open(file_path, 'rb')
        device = alsaaudio.PCM()
        logger.debug("[PyAlsaAudioPlayer] %d channels, %d sampling rate" % (f.getnchannels(),
                                                                            f.getframerate()))

        # Set attributes
        device.setchannels(f.getnchannels())
        device.setrate(f.getframerate())

        # 8bit is unsigned in wav files
        if f.getsampwidth() == 1:
            device.setformat(alsaaudio.PCM_FORMAT_U8)
        # Otherwise we assume signed data, little endian
        elif f.getsampwidth() == 2:
            device.setformat(alsaaudio.PCM_FORMAT_S16_LE)
        elif f.getsampwidth() == 3:
            device.setformat(alsaaudio.PCM_FORMAT_S24_LE)
        elif f.getsampwidth() == 4:
            device.setformat(alsaaudio.PCM_FORMAT_S32_LE)
        else:
            raise ValueError('Unsupported format')

        periodsize = f.getframerate() / 8

        device.setperiodsize(periodsize)

        data = f.readframes(periodsize)
        while data:
            # Read data from stdin
            device.write(data)
            data = f.readframes(periodsize)
