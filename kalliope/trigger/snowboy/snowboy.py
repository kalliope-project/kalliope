import logging
import time

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

        # get the pmdl file to load
        self.pmdl = kwargs.get('pmdl_file', None)

        if self.pmdl is None:
            raise MissingParameterException("Pmdl file is required with snowboy")

        self.detector = snowboydecoder.HotwordDetector(self.pmdl, sensitivity=0.5, detected_callback=self.callback,
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
