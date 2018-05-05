import speech_recognition as sr

from kalliope.core import Utils
from kalliope.stt.Utils import SpeechRecognition


class Houndify(SpeechRecognition):

    def __init__(self, callback=None, **kwargs):
        """
        Start recording the microphone and analyse audio with Houndify api
        :param callback: The callback function to call to send the text
        :param kwargs:
        """
        # give the audio file path to process directly to the mother class if exist
        SpeechRecognition.__init__(self, kwargs.get('audio_file_path', None))

        # callback function to call after the translation speech/tex
        self.main_controller_callback = callback
        self.client_id = kwargs.get('client_id', None)
        self.key = kwargs.get('key', None)
        # only english supported
        # self.language = kwargs.get('language', "en-US")
        self.show_all = kwargs.get('show_all', False)

        # start listening in the background
        self.set_callback(self.houndify_callback)
        # start processing, record a sample from the microphone if no audio file path provided, else read the file
        self.start_processing()

    def houndify_callback(self, recognizer, audio):
        """
        called from the background thread
        """
        try:
            captured_audio = recognizer.recognize_houndify(audio,
                                                           client_id=self.client_id,
                                                           client_key=self.key,
                                                           show_all=self.show_all)
            Utils.print_success("Houndify Speech Recognition thinks you said %s" % captured_audio)
            self._analyse_audio(captured_audio)

        except sr.UnknownValueError:
            Utils.print_warning("Houndify Speech Recognition could not understand audio")
            # callback anyway, we need to listen again for a new order
            self._analyse_audio(audio_to_text=None)
        except sr.RequestError as e:
            Utils.print_danger("Could not request results from Houndify Speech Recognition service; {0}".format(e))
            # callback anyway, we need to listen again for a new order
            self._analyse_audio(audio_to_text=None)
        except AssertionError:
            Utils.print_warning("No audio caught from microphone")
            self._analyse_audio(audio_to_text=None)

    def _analyse_audio(self, audio_to_text):
        """
        Confirm the audio exists and run it in a Callback
        :param audio_to_text: the captured audio
        """
        if self.main_controller_callback is not None:
            self.main_controller_callback(audio_to_text)
