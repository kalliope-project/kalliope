from threading import Thread
from time import sleep

import logging
import speech_recognition as sr

from kalliope import Utils, SettingLoader
from kalliope.core.Utils.RpiUtils import RpiUtils

logging.basicConfig()
logger = logging.getLogger("kalliope")


class SpeechRecognition(Thread):

    def __init__(self, audio_file=None):
        """
        Thread used to caught n audio from the microphone and pass it to a callback method
        """
        super(SpeechRecognition, self).__init__()
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.callback = None
        self.stop_thread = None
        self.kill_yourself = False
        self.audio_stream = None

        # get global configuration
        sl = SettingLoader()
        self.settings = sl.settings

        if audio_file is None:
            # audio file not set, we need to capture a sample from the microphone
            with self.microphone as source:
                # we only need to calibrate once, before we start listening
                self.recognizer.adjust_for_ambient_noise(source)
        else:
            # audio file provided
            with sr.AudioFile(audio_file) as source:
                self.audio_stream = self.recognizer.record(source)  # read the entire audio file

    def run(self):
        """
        Start the thread that listen the microphone and then give the audio to the callback method
        """
        if self.audio_stream is None:
            Utils.print_info("Say something!")
            # Turn on the listening led if we are on a Raspberry
            if self.settings.rpi_settings:
                if self.settings.rpi_settings.pin_led_listening:
                    RpiUtils.switch_pin_to_on(self.settings.rpi_settings.pin_led_listening)
            self.stop_thread = self.recognizer.listen_in_background(self.microphone, self.callback)
            while not self.kill_yourself:
                sleep(0.1)
            logger.debug("kill the speech recognition process")
            self.stop_thread()
        else:
            self.callback(self.recognizer, self.audio_stream)

    def start_processing(self):
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
