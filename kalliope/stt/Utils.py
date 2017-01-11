import speech_recognition as sr

from kalliope import Utils


class SpeechRecognition(object):

    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.stop_listening = None
        with self.microphone as source:
            # we only need to calibrate once, before we start listening
            self.recognizer.adjust_for_ambient_noise(source)

    def start_listening(self, callback):
        Utils.print_info("Say something!")
        self.recognizer.listen_in_background(self.microphone, callback=callback)

    def interrupt(self):
        self.stop_listening()
