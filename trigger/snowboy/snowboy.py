from trigger.snowboy import snowboydecoder


class MissingParameterException(Exception):
    pass


class Snowboy(object):

    def __init__(self, **kwargs):
        print "loaded"
        # pause listening boolean
        self.interrupted = False

        # callback function to call when hotword caught
        self.callback = kwargs.get('callback', None)
        if self.callback is None:
            raise MissingParameterException("callback function is required with snowboy")

        # get the pmdl file to load
        self.pmdl = kwargs.get('pmdl_file', None)

        if self.pmdl is None:
            raise MissingParameterException("Pmdl file is required with snowboy")

    def interrupt_callback(self):
        """
        This function will be passed to snowboy to stop the main thread
        :return:
        """
        return self.interrupted

    def start(self):
        """
        Start the snowboy thread and wait for a Jarvis trigger word
        :return:
        """
        print "started"
        detector = snowboydecoder.HotwordDetector(self.pmdl, sensitivity=0.5)

        # start snowboy loop
        detector.start(detected_callback=self.callback,
                       interrupt_check=self.interrupt_callback,
                       sleep_time=0.03)

        # we wait that a callback
        detector.terminate()

    def pause(self):
        """
        Stop the Snowboy main thread
        :return:
        """
        self.interrupted = True

    def unpause(self):
        self.interrupted = False
