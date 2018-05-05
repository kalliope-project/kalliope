from threading import Thread

import logging
import speech_recognition as sr

from kalliope import Utils, SettingLoader

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
                if self.settings.options.adjust_for_ambient_noise_second > 0:
                    # threshold is calculated from capturing ambient sound
                    logger.debug("[SpeechRecognition] threshold calculated by "
                                 "capturing ambient noise during %s seconds" %
                                 self.settings.options.adjust_for_ambient_noise_second)
                    Utils.print_info("[SpeechRecognition] capturing ambient sound during %s seconds" %
                                     self.settings.options.adjust_for_ambient_noise_second)
                    self.recognizer.adjust_for_ambient_noise(source,
                                                             duration=self.settings.
                                                             options.adjust_for_ambient_noise_second)
                else:
                    # threshold is defined manually
                    logger.debug("[SpeechRecognition] threshold defined by settings: %s" %
                                 self.settings.options.energy_threshold)
                    self.recognizer.energy_threshold = self.settings.options.energy_threshold

                Utils.print_info("[SpeechRecognition] Threshold set to: %s" % self.recognizer.energy_threshold)
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
            try:
                with self.microphone as source:
                    logger.debug("[SpeechRecognition] STT timeout: %s" % self.settings.options.stt_timeout)
                    self.audio_stream = self.recognizer.listen(source, timeout=self.settings.options.stt_timeout)
            except sr.WaitTimeoutError:
                logger.debug("[SpeechRecognition] timeout reached while waiting for audio input")
                self.audio_stream = None
            logger.debug("[SpeechRecognition] end of speech recognition process")

            self.callback(self.recognizer, self.audio_stream)

    def start_processing(self):
        """
        A method to start the thread
        """
        self.start()

    def set_callback(self, callback):
        """
        set the callback method that will receive the audio stream caught by the microphone
        :param callback: callback method
        :return:
        """
        self.callback = callback
