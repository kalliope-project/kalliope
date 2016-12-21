import logging
import os
from threading import Thread

from cffi import FFI as _FFI

from kalliope.core.Utils.Utils import Utils
from kalliope.core.ConfigurationManager import SettingLoader

logging.basicConfig()
logger = logging.getLogger("kalliope")


class OrderListener(Thread):
    """
    This Class allows to Listen to an Incoming voice order.

    .. notes:: Thread are used to calibrate the sound of the microphone input with the noise while
        starting to listen the incoming order. Basically it avoids delays.
    """

    def __init__(self, callback=None, stt=None):
        """
        This class is called after we catch the hotword that has woken up Kalliope.
        We now wait for an order spoken out loud by the user, translate the order into a text and run the action
         attached to this order from settings
        :param callback: callback function to call
        :type callback: Callback function
        :param stt: Speech to text plugin name to load. If not provided,
        :type stt: STT instance
        we will load the default one set in settings

        .. seealso::  STT
        """
        # this is a trick to ignore ALSA output error
        # see http://stackoverflow.com/questions/7088672/pyaudio-working-but-spits-out-error-messages-each-time
        super(OrderListener, self).__init__()
        self.stt = stt
        self._ignore_stderr()
        self.stt_module_name = stt
        self.callback = callback
        sl = SettingLoader()
        self.settings = sl.settings

    def run(self):
        """
        Start thread
        """
        self.load_stt_plugin()

    def load_stt_plugin(self):
        if self.stt is None:
            self.stt_module_name = self.settings.default_stt_name

        for stt_object in self.settings.stts:
            if stt_object.name == self.stt_module_name:
                stt_object.parameters["callback"] = self.callback
                Utils.get_dynamic_class_instantiation(package_name='stt',
                                                      module_name=stt_object.name.capitalize(),
                                                      parameters=stt_object.parameters)

    @staticmethod
    def _ignore_stderr():
        """
        Try to forward PortAudio messages from stderr to /dev/null.
        """
        ffi = _FFI()
        ffi.cdef("""
        /* from stdio.h */
        FILE* fopen(const char* path, const char* mode);
        int fclose(FILE* fp);
        FILE* stderr;  /* GNU C library */
        FILE* __stderrp;  /* Mac OS X */
        """)
        stdio = ffi.dlopen(None)
        devnull = stdio.fopen(os.devnull.encode(), b'w')
        try:
            stdio.stderr = devnull
        except KeyError:
            try:
                stdio.__stderrp = devnull
            except KeyError:
                stdio.fclose(devnull)
