# -*- coding: utf-8 -*-
import alsaaudio
import logging
import wave

logging.basicConfig()
logger = logging.getLogger("kalliope")

CHUNK = 1024

ALSAAUDIO_BIT_MAPPING = {8:  alsaaudio.PCM_FORMAT_S8,
                         16: alsaaudio.PCM_FORMAT_S16_LE,
                         24: alsaaudio.PCM_FORMAT_S24_LE,
                         32: alsaaudio.PCM_FORMAT_S32_LE}

STANDARD_SAMPLE_RATES = (
    8000, 9600, 11025, 12000, 16000, 22050, 24000, 32000, 44100, 48000, 88200,
    96000, 192000
)

DEVICE_TYPE_ALL = 'all'
DEVICE_TYPE_INPUT = 'input'
DEVICE_TYPE_OUTPUT = 'output'


def bits_to_samplefmt(bits):
    if bits in ALSAAUDIO_BIT_MAPPING.keys():
        return ALSAAUDIO_BIT_MAPPING[bits]
    else: 
        raise ValueError('Unsupported format')


class Pyalsaaudio(object):
    """
    This Class is representing the Player Object used to play the all sound of the system.
    """

    def __init__(self, **kwargs):
        # List devices
        logger.debug("[pyalsaaudio.__init__] instance")
        logger.debug("[pyalsaaudio.__init__] devices : %s " % (str(self.get_devices(DEVICE_TYPE_OUTPUT))))
        logger.debug("[pyalsaaudio.__init__] args : %s " % str(kwargs))
        self.device = kwargs.get('device', 'default')

    @staticmethod
    def get_devices(device_type=DEVICE_TYPE_ALL):
        devices = set()
        if device_type in (DEVICE_TYPE_ALL,
                           DEVICE_TYPE_OUTPUT):
            devices.update(set(alsaaudio.pcms(alsaaudio.PCM_PLAYBACK)))
        if device_type in (DEVICE_TYPE_ALL,
                           DEVICE_TYPE_INPUT):
            devices.update(set(alsaaudio.pcms(alsaaudio.PCM_CAPTURE)))
        device_names = sorted(list(devices))
        num_devices = len(device_names)
        logger.debug('Found %d ALSA devices', num_devices)
        return device_names

    def play(self, file_path):

        f = wave.open(file_path, 'rb')
        pcm_type = alsaaudio.PCM_PLAYBACK
        stream = alsaaudio.PCM(type=pcm_type,
                               mode=alsaaudio.PCM_NORMAL,
                               device=self.device)  # this is just for testing
                               # device='sysdefault:CARD=ALSA')  # this is just for testing
                                # on RPI3 this is fine; pulse (usually also default) is not working
                                # device should be configurable; default schould be "default"
        # Set attributes
        stream.setchannels(f.getnchannels())
        stream.setrate(f.getframerate())
        bits = f.getsampwidth()*8
        stream.setformat(bits_to_samplefmt(bits))        
        stream.setperiodsize(CHUNK)
        
        logger.debug("[PyAlsaAudioPlayer] %d channels, %d sampling rate, %d bit" % (f.getnchannels(),
                                                                            f.getframerate(),  bits))
        
        data = f.readframes(CHUNK)
        while data:
            # Read data from stdin
            stream.write(data)
            data = f.readframes(CHUNK)
     
        f.close()
        stream.close()
