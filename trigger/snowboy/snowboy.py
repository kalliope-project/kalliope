import logging
import time
import inspect
import os

from trigger.snowboy import snowboydecoder


class MissingParameterException(Exception):
    pass

logging.basicConfig()
logger = logging.getLogger("kalliope")


class Snowboy(object):

    def __init__(self, **kwargs):
        # pause listening boolean
        self.interrupted = False
        self.kill_received = False

        # callback function to call when hotword caught
        self.callback = kwargs.get('callback', None)
        if self.callback is None:
            raise MissingParameterException("callback function is required with snowboy")

        # get the pmdl file from the config
        self.pmdl = kwargs.get('pmdl_file', None)

        # if no pmdl file in the config raise exception
        if self.pmdl is None:
            raise MissingParameterException("Pmdl file is required with snowboy")

        # else guess the pmdl path from root of kalliope module
        self.pmdl_path = self._get_root_pmdl_path(self.pmdl)

        self.detector = snowboydecoder.HotwordDetector(self.pmdl_path, sensitivity=0.5, detected_callback=self.callback,
                                                       interrupt_check=self.interrupt_callback,
                                                       sleep_time=0.03)

    def interrupt_callback(self):
        """
        This function will be passed to snowboy to stop the main thread
        :return:
        """
        return self.interrupted

    def start(self):
        """
        Start the snowboy thread and wait for a Kalliope trigger word
        :return:
        """
        # start snowboy loop
        self.detector.daemon = True
        try:
            self.detector.start()
            while not self.kill_received:
                #  once the main thread has started child thread, there's nothing else for it to do.
                # So it exits, and the threads are destroyed instantly. So let's keep the main thread alive
                time.sleep(1)
        except KeyboardInterrupt:
            self.kill_received = True
            self.detector.kill_received = True
        # we wait that a callback
        self.detector.terminate()

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
    def _get_root_pmdl_path(pmdl_file):
        """
        Return the full path of the pmdl file

        :Example:

            pmdl_path = cls._get_root_pmdl_path(pmdl_file)

        .. raises:: IOError
        .. warnings:: Static method and Private
        """

        # get current script directory path. We are in /an/unknown/path/kalliope/trigger/snowboy
        cur_script_directory = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        # get parent dir. Now we are in /an/unknown/path/kalliope
        parent_dir = os.path.normpath(cur_script_directory + os.sep + os.pardir + os.sep + os.pardir)
        pmdl_path = parent_dir + os.sep + pmdl_file
        logger.debug("Real pmdl_file path: %s" % pmdl_path)
        if os.path.isfile(pmdl_path):
            return pmdl_path
        raise IOError("Pmdl file not found: %s" % pmdl_path)
