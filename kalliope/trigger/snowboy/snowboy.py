import logging
import os
from threading import Thread

from kalliope import Utils
from kalliope.trigger.snowboy import snowboydecoder
from cffi import FFI as _FFI


class SnowboyModelNotFound(Exception):
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

        # get the sensitivity if set by the user
        self.sensitivity = kwargs.get('sensitivity', 0.5)
        self.apply_frontend = kwargs.get('apply_frontend', False)

        # callback function to call when hotword caught
        self.callback = kwargs.get('callback', None)
        if self.callback is None:
            raise MissingParameterException("callback function is required with snowboy")

        # get the keywords to load
        self.keywords = kwargs.get('keywords', None)

        self.pmdl_file = kwargs.get('pmdl_file', None)  # We notify the user that the pmdl_file parameter has been changed
        if self.pmdl_file:
            raise MissingParameterException('"pmdl_file" parameter is deprecated, please update your snowboy settings. \n Visit https://kalliope-project.github.io/kalliope/settings/triggers/snowboy/ for more information.')

        if self.keywords is None:
            raise MissingParameterException("At least one keyword is required with snowboy")

        keyword_files = list()
        sensitivities = list()
        for keyword in self.keywords:
            if self.check_if_path_is_valid(keyword['file_path']):
                keyword_files.append(keyword['file_path'])
            try:
                if not isinstance(keyword['sensitivity'], list):
                    sensitivities.append(keyword['sensitivity'])
                else:
                    for sensitivity in keyword['sensitivity']:
                        sensitivities.append(sensitivity)
            except KeyError:
                sensitivities.append(0.5)

        self.detector = snowboydecoder.HotwordDetector(keyword_files,
                                                       sensitivity=sensitivities,
                                                       detected_callback=self.callback,
                                                       interrupt_check=self.interrupt_callback,
                                                       apply_frontend=self.apply_frontend)

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
        self.detector.pause()

    def unpause(self):
        """
        unpause the Snowboy main thread
        """
        logger.debug("Unpausing snowboy process")
        self.detector.unpause()

    def stop(self):
        """
        Kill the snowboy process
        :return: 
        """
        logger.debug("Killing snowboy process")
        self.interrupted = True
        self.detector.terminate()


    def check_if_path_is_valid(self, keyword_file):
        try:
            keyword_path = Utils.get_real_file_path(keyword_file)
            os.path.isfile(keyword_path)
        except TypeError: 
            raise SnowboyModelNotFound("The keyword at %s does not exist" % keyword_file)
        return True

    @staticmethod
    def _ignore_stderr():
        """
        Try to forward PortAudio messages from stderr to /dev/null.
        """
        ffi = _FFI()
        ffi.cdef("""
            /* from stdio.h */
            extern FILE* fopen(const char* path, const char* mode);
            extern int fclose(FILE* fp);
            extern FILE* stderr;  /* GNU C library */
            extern FILE* __stderrp;  /* Mac OS X */
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
