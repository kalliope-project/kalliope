import speech_recognition as sr

from core import Utils
from core.OrderListener import OrderListener


class Houndify(OrderListener):

    def __init__(self, callback=None, **kwargs):
        """
        Start recording the microphone and analyse audio with Houndify api
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

        # recognize speech using Houndify Speech Recognition
        try:
            client_id = kwargs.get('client_id', None)
            key = kwargs.get('key', None)
            language = kwargs.get('language', "en-US")
            show_all = kwargs.get('show_all', False)

            captured_audio = r.recognize_houndify(audio, client_id=client_id, client_key=key,
                                                  language=language, show_all=show_all)
            Utils.print_success("Houndify Speech Recognition thinks you said %s" % captured_audio)
            self._analyse_audio(captured_audio)

        except sr.UnknownValueError:
            Utils.print_warning("Houndify Speech Recognition could not understand audio")
            # callback anyway, we need to listen again for a new order
            self._analyse_audio(audio=None)
        except sr.RequestError as e:
            Utils.print_danger("Could not request results from Houndify Speech Recognition service; {0}".format(e))
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
