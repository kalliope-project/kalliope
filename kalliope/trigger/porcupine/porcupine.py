import logging
import os
from threading import Thread

from kalliope import Utils
from kalliope.trigger.porcupine import porcupinedecoder
from cffi import FFI as _FFI


class PorcupineWakeWordNotFound(Exception):
    pass


class MissingParameterException(Exception):
    pass

logging.basicConfig()
logger = logging.getLogger("kalliope")


class Porcupine(Thread):

    def __init__(self, **kwargs):
        super(Porcupine, self).__init__()
        self._ignore_stderr()
        # Pause listening boolean.
        self.kill_received = False

        # Get the sensitivity if set by the user.
        self.sensitivities = kwargs.get('sensitivity', 0.5)
        # Get input device if set by the user.
        self.input_device_index = kwargs.get('input_device_index', None)
        # Use tiny keywords if user set to True.
        self.tiny_keyword = kwargs.get('tiny_keyword', False)
        # Callback function to call when hotword caught.
        self.callback = kwargs.get('callback', None)
        if self.callback is None:
            raise MissingParameterException("callback function is required with porcupine")

        # Get the keyword to load.
        self.keyword = kwargs.get('keyword', None)
        if self.keyword is None:
            raise MissingParameterException("Keyword is required with porcupine")

        # We can use more then one wake word, in this case we seperate them and get the keyword paths.    
        if isinstance(self.keyword, (list,)):
            for keyword in self.keyword:
                path = Utils.get_real_file_path(keyword)                
                try:
                    os.path.isfile(path)
                except TypeError: 
                    raise PorcupineWakeWordNotFound("The porcupine keyword at %s does not exist" % keyword)
            keyword_file_paths = ", ".join(self.keyword)
        
        # No need to seperate, we just check if keyword exist.
        else:
            keyword_file_paths = Utils.get_real_file_path(self.keyword)
            try:
                os.path.isfile(keyword_file_paths)
            except TypeError:        
                raise PorcupineWakeWordNotFound("The porcupine keyword at %s does not exist" % self.keyword)
        
        if self.sensitivities is None:
            raise MissingParameterException("sensitivities is required with porcupine")
        
        # If there are more sensitivities we also seperate them.      
        if isinstance(self.sensitivities, (list,)):
            # If the user has set less sensitivties than keywords, we add 0.5 as default.
            if len(self.keyword) > len(self.sensitivities):
                for item in self.sensitivities:            
                    while len(self.keyword) > len(self.sensitivities):
                        self.sensitivities.append(0.5)

            self.sensitivities = ", ".join(map(str, self.sensitivities))

        self.detector = porcupinedecoder.HotwordDetector(keyword_file_paths=keyword_file_paths,
                                                        sensitivities=self.sensitivities,
                                                        input_device_index=self.input_device_index,
                                                        tiny=self.tiny_keyword,
                                                        detected_callback=self.callback
                                                        )

    def run(self):
        """
        Start the porcupine thread and wait for a Kalliope trigger word
        :return:
        """
        # start porcupine loop forever
        self.detector.daemon = True
        self.detector.start()
        self.detector.join()

    def pause(self):
        """
        pause the porcupine main thread
        """
        logger.debug("[Porcupine] Pausing porcupine process")
        self.detector.paused = True

    def unpause(self):
        """
        unpause the porcupine main thread
        """
        logger.debug("[Porcupine] Unpausing porcupine process")
        self.detector.paused = False

    def stop(self):
        """
        Kill the porcupine process
        :return: 
        """
        logger.debug("[Porcupine] Killing porcupine process")
        self.interrupted = True
        self.detector.terminate()

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
