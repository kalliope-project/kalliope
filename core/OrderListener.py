import speech_recognition as sr


class OrderListener:

    def __init__(self, main_controller=None):
        """
        This class is called after we catch the hotword that have woke up JARVIS.
        We now wait for an order spoken out loud by the user, translate the order into a text and run the action
         attached to this order from settings
        :param main_controller:
        :type main_controller: MainController
        """
        self.main_controller = main_controller

    def start(self):
        """
        Start recording the microphone
        :return:
        """
        # obtain audio from the microphone
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Say something!")
            audio = r.listen(source)

        # recognize speech using Google Speech Recognition
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))