import inspect
import logging
import os
import time
from threading import Thread

from kalliope import Utils
from kalliope.trigger.snowboy import snowboydecoder
from cffi import FFI as _FFI


class SnowboyModelNotFounfd(Exception):
    pass


class MissingParameterException(Exception):
    pass

logging.basicConfig()
logger = logging.getLogger("kalliope")


class Snowboy(Thread):

    def __init__(self, **kwargs):
        super(Snowboy, self).__init__()
        self._ignore_stderr()
        # pause listening boolean
        self.interrupted = False
        self.kill_received = False

        # callback function to call when hotword caught
        self.callback = kwargs.get('callback', None)
        if self.callback is None:
            raise MissingParameterException("callback function is required with snowboy")

        # get the pmdl file to load
        self.pmdl = kwargs.get('pmdl_file', None)
        if self.pmdl is None:
            raise MissingParameterException("Pmdl file is required with snowboy")

        self.pmdl_path = Utils.get_real_file_path(self.pmdl)
        if not os.path.isfile(self.pmdl_path):
            raise SnowboyModelNotFounfd("The snowboy model file %s does not exist" % self.pmdl_path)

        self.detector = snowboydecoder.HotwordDetector(self.pmdl_path, sensitivity=0.5, detected_callback=self.callback,
                                                       interrupt_check=self.interrupt_callback,
                                                       sleep_time=0.03)

    def interrupt_callback(self):
        """
        This function will be passed to snowboy to stop the main thread
        :return:
        """
        return self.interrupted

    def run(self):
        """
        Start the snowboy thread and wait for a Kalliope trigger word
        :return:
        """
        # start snowboy loop forever
        self.detector.daemon = True
        self.detector.start()
        self.detector.join()

    def pause(self):
        """
        pause the Snowboy main thread
        """
        logger.debug("Pausing snowboy process")
        self.detector.paused = True

    def unpause(self):
        """
        unpause the Snowboy main thread
        """
        logger.debug("Unpausing snowboy process")
        self.detector.paused = False

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