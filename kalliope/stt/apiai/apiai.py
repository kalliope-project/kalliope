import speech_recognition as sr

from kalliope.core import Utils
from kalliope.core.OrderListener import OrderListener


class Apiai(OrderListener):

    def __init__(self, callback=None, **kwargs):
        """
        Start recording the microphone and analyse audio with Apiai api
        :param callback: The callback function to call to send the text
        :param kwargs:
        """
        OrderListener.__init__(self)

        # callback function to call after the translation speech/tex
        self.callback = callback
        # obtain audio from the microphone
        r = sr.Recognizer()
        with sr.Microphone() as source:
            # listen for 1 second to calibrate the energy threshold for ambient noise levels
            r.adjust_for_ambient_noise(source)
            Utils.print_info("Say something!")
            audio = r.listen(source)

        # recognize speech using Apiai Speech Recognition
        try:

            key = kwargs.get('key', None)
            language = kwargs.get('language', "en")
            session_id= kwargs.get('session_id', None)
            show_all = kwargs.get('show_all', False)

            captured_audio = r.recognize_api(audio, client_access_token=key, language=language, session_id=session_id, show_all=show_all)
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
        Confirm the audio exists annd run it in a Callback
        :param audio: the captured audio
        """
        # if self.main_controller is not None:
        #     self.main_controller.analyse_order(audio)
        if self.callback is not None:
            self.callback(audio)
