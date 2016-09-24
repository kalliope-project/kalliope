import speech_recognition as sr
from core.OrderListener import OrderListener


class Google(OrderListener):

    def __init__(self, main_controller=None, **kwargs):
        OrderListener.__init__(self, main_controller)

        """
        Start recording the microphone
        :return:
        """
        # obtain audio from the microphone
        r = sr.Recognizer()
        with sr.Microphone() as source:
            # listen for 1 second to calibrate the energy threshold for ambient noise levels
            r.adjust_for_ambient_noise(source)
            print("Say something!")
            audio = r.listen(source)

        # recognize speech using Google Speech Recognition
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`

            key = kwargs.get('key', None)
            language = kwargs.get('language', "en-US")
            show_all = kwargs.get('show_all', False)

            captured_audio = r.recognize_google(audio, key=key, language=language, show_all=show_all)
            print "Google Speech Recognition thinks you said %s" % captured_audio
            self._analyse_audio(captured_audio)

        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

    def _analyse_audio(self, audio):
        if self.main_controller is not None:
            self.main_controller.analyse_order(audio)
