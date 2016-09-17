from stt.snowboy import snowboydecoder


class JarvisTrigger:
    """
    Class used to catch the trigger word before listening for an order to process
    """
    def __init__(self, main_controller):
        """

        :param main_controller: Main controller of the app
        :type main_controller MainController
        """
        self.main_controller = main_controller
        # TODO update this to load the file from settings
        self.model = "stt/snowboy/resources/jarviss.pmdl"
        # boolean used to stop the snowbow listening
        self.interrupted = False

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

        detector = snowboydecoder.HotwordDetector(self.model, sensitivity=0.5)

        # start snowboy loop
        detector.start(detected_callback=self.main_controller.hotword_detected,
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