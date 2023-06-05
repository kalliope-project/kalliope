import threading
from threading import Thread
from time import time
import logging
from kalliope import Utils, SettingLoader
from kalliope.stt import SpeechRecognizer
from kalliope.core.HookManager import HookManager
import speech_recognition as sr

logging.basicConfig()
logger = logging.getLogger("kalliope")

class SpeechRecognition(Thread):

    def __init__(self, audio_file=None):
        """
        Thread used to process n audio file and pass it to a callback method
        """
        super(SpeechRecognition, self).__init__()
        self.callback = None
        self.audio_stream = None
        # get global configuration
        sl = SettingLoader()
        self.settings = sl.settings
        self.recognizer = SpeechRecognizer.ResponsiveRecognizer(multiplier=self.settings.options.recognizer_multiplier, 
                                                                energy_ratio=self.settings.options.recognizer_energy_ratio,
                                                                recording_timeout=self.settings.options.recognizer_recording_timeout,
                                                                recording_timeout_with_silence=self.settings.options.recognizer_recording_timeout_with_silence)

        if audio_file is None:
            # audio file not set, we need to capture a sample from the microphone
            self.microphone = SpeechRecognizer.MutableMicrophone()

        else:
            # audio file provided
            with sr.AudioFile(audio_file) as source:
                self.audio_stream = self.recognizer.record(source) # read the entire audio file

    def run(self):
        """
        Start the thread that listen the microphone and then give the audio to the callback method
        """
        if self.audio_stream is None:
            HookManager.on_start_listening()
            Utils.print_success("Say something!")
            time_start = time()
            with self.microphone as source:
                self.audio_stream = self.recognizer.listen(source)
            secs = time() - time_start
            HookManager.on_stop_listening()
            Utils.print_success(f"Finished listening ({secs} seconds)!")

        HookManager.on_start_stt_processing()
        Utils.print_success("Processing via STT engine!")
        time_start = time()
        self.callback(self.recognizer, self.audio_stream)
        secs = time() - time_start
        HookManager.on_stop_stt_processing()
        Utils.print_success(f"Finished processing ({secs} seconds)!")

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
        
