from threading import Thread
from time import sleep

import logging
import speech_recognition as sr

from kalliope import Utils

logging.basicConfig()
logger = logging.getLogger("kalliope")


class SpeechRecognition(Thread):

    def __init__(self):
        """
        Thread used to caught n audio from the microphone and pass it to a callback method
        """
        super(SpeechRecognition, self).__init__()
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.callback = None
        self.stop_listening = None
        self.kill_yourself = False
        with self.microphone as source:
            # we only need to calibrate once, before we start listening
            self.recognizer.adjust_for_ambient_noise(source)

    def run(self):
        """
        Start the thread that listen the microphone and then give the audio to the callback method
        """
        Utils.print_info("Say something!")
        self.stop_listening = self.recognizer.listen_in_background(self.microphone, self.callback)
        while not self.kill_yourself:
            sleep(0.1)
        logger.debug("kill the speech recognition process")
        self.stop_listening()

    def start_listening(self):
        """
        A method to start the thread
        """
        self.start()

    def stop_listening(self):
        self.kill_yourself = True

    def set_callback(self, callback):
        """
        set the callback method that will receive the audio stream caught by the microphone
        :param callback: callback method
        :return:
        """
        self.callback = callback
