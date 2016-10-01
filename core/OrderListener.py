import logging
import os
from cffi import FFI as _FFI
import sys

from core import ConfigurationManager

logging.basicConfig()
logger = logging.getLogger("jarvis")


class OrderListener:

    def __init__(self, callback=None, stt=None):
        """
        This class is called after we catch the hotword that have woke up JARVIS.
        We now wait for an order spoken out loud by the user, translate the order into a text and run the action
         attached to this order from settings
        :param callback: callback function to call
        :param stt: Speech to text plugin name to load. If not provided,
        we will load the default one set in settings
        """
        # this is a trick to ignore ALSA output error
        # see http://stackoverflow.com/questions/7088672/pyaudio-working-but-spits-out-error-messages-each-time
        self._ignore_stderr()
        self.stt = stt
        self.callback = callback
        # self.settings = main_controller.conf.settingLoader.get_config()
        self.settings = ConfigurationManager().get_settings()

    def load_stt_plugin(self):
        if self.stt is None:
            self.stt = ConfigurationManager.get_default_speech_to_text()

        stt_args = ConfigurationManager.get_stt_args(self.stt)

        # capitalizes the first letter (because classes have first letter upper case)
        default_stt_plugin = self.stt.capitalize()
        self._run_stt_plugin(default_stt_plugin, stt_args)

    def _run_stt_plugin(self, stt_plugin, parameters=None):
        """
        Dynamic loading of a STT module
        :param stt_plugin: Module name to load
        :param parameters: Parameter of the module
        :return:
        """
        logger.debug("Running STT %s with parameter %s" % (stt_plugin, parameters))
        mod = __import__('stt', fromlist=[stt_plugin])

        klass = getattr(mod, stt_plugin)

        if klass is not None:
            # run the plugin
            if not parameters:
                klass(self.callback)
            elif isinstance(parameters, dict):
                klass(self.callback, **parameters)
            else:
                klass(self.callback, parameters)

    @staticmethod
    def _ignore_stderr():
        """Try to forward PortAudio messages from stderr to /dev/null."""
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


