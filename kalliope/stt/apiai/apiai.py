import speech_recognition as sr

from kalliope.core import Utils
from kalliope.stt.Utils import SpeechRecognition


class Apiai(SpeechRecognition):

    def __init__(self, callback=None, **kwargs):
        """
        Start recording the microphone and analyse audio with Apiai api
        :param callback: The callback function to call to send the text
        :param kwargs:
        """
        SpeechRecognition.__init__(self)

        # callback function to call after the translation speech/tex
        self.callback = callback
        self.key = kwargs.get('key', None)
        self.language = kwargs.get('language', "en")
        self.session_id = kwargs.get('session_id', None)
        self.show_all = kwargs.get('show_all', False)

        # start listening in the background
        self.stop_listening = self.start_listening(self.apiai_callback)

    def apiai_callback(self, recognizer, audio):
        """
        called from the background thread
        :param recognizer:
        :param audio:
        :return:
        """
        try:
            captured_audio = recognizer.recognize_api(audio,
                                                      client_access_token=self.key,
                                                      language=self.language,
                                                      session_id=self.session_id,
                                                      show_all=self.show_all)
            Utils.print_success("Apiai Speech Recognition thinks you said %s" % captured_audio)
            self._analyse_audio(captured_audio)

        except sr.UnknownValueError as e:
            Utils.print_warning("Apiai Speech Recognition could not understand audio; {0}".format(e))
            # callback anyway, we need to listen again for a new order
            self._analyse_audio(audio=None)
        except sr.RequestError as e:
            Utils.print_danger("Could not request results from Apiai Speech Recognition service; {0}".format(e))
            # callback anyway, we need to listen again for a new order
            self._analyse_audio(audio=None)

    def _analyse_audio(self, audio):
        """
        Confirm the audio exists and run it in a Callback
        :param audio: the captured audio
        """
        if self.callback is not None:
            self.callback(audio)
