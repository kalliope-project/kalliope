import speech_recognition as sr

from kalliope.core import Utils
from kalliope.stt.Utils import SpeechRecognition


class Wit(SpeechRecognition):

    def __init__(self, callback=None, **kwargs):
        """
        Start recording the microphone and analyse audio with Wit.ai api
        :param callback: The callback function to call to send the text
        :param kwargs:
        """
        SpeechRecognition.__init__(self)

        # callback function to call after the translation speech/tex
        self.callback = callback
        self.key = kwargs.get('key', None)
        self.show_all = kwargs.get('show_all', False)

        # start listening in the background
        self.stop_listening = self.start_listening(self.wit_callback)

    def wit_callback(self, recognizer, audio):
        try:
            captured_audio = recognizer.recognize_wit(audio,
                                                      key=self.key,
                                                      show_all=self.show_all)
            Utils.print_success("Wit.ai Speech Recognition thinks you said %s" % captured_audio)
            self._analyse_audio(captured_audio)

        except sr.UnknownValueError:
            Utils.print_warning("Wit.ai Speech Recognition could not understand audio")
            # callback anyway, we need to listen again for a new order
            self._analyse_audio(audio=None)
        except sr.RequestError as e:
            Utils.print_danger("Could not request results from Wit.ai Speech Recognition service; {0}".format(e))
            # callback anyway, we need to listen again for a new order
            self._analyse_audio(audio=None)

    def _analyse_audio(self, audio):
        """
        Confirm the audio exists annd run it in a Callback
        :param audio: the captured audio
        """

        # if self.main_controller is not None:
        #     self.main_controller.analyse_order(audio)
        if self.callback is not None:
            self.callback(audio)
