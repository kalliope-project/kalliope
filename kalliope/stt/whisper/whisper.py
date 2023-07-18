import speech_recognition as sr
import re

from kalliope.core import Utils
from kalliope.stt.Utils import SpeechRecognition


class Whisper(SpeechRecognition):

    def __init__(self, callback=None, **kwargs):
        """
        Start recording the microphone and analyse audio with CMU whisper api
        :param callback: The callback function to call to send the text
        :param kwargs:
        """
        # give the audio file path to process directly to the mother class if exist
        SpeechRecognition.__init__(self, kwargs.get('audio_file_path', None))

        # callback function to call after the translation speech/tex
        self.main_controller_callback = callback

        self.model = kwargs.get('model', 'tiny')
        self.language = kwargs.get('language', None)
        self.unformat = kwargs.get('unformat', True)
        self.unformat_characters = kwargs.get('unformat_characters', [])
        self.translate = kwargs.get('translate', False)

        # start listening in the background
        self.set_callback(self.whisper_callback)
        # start processing, record a sample from the microphone if no audio file path provided, else read the file
        self.start_processing()

    def whisper_callback(self, recognizer, audio):
        """
        called from the background thread
        """
        try:
            response = recognizer.recognize_whisper(audio,
                                                   model=self.model,
                                                   language=self.language,
                                                   translate=self.translate,
                                                   show_dict=True)
            captured_audio = response.get('text').strip()
            captured_language = response.get('language')
            if self.unformat:
                captured_audio = captured_audio.lower()
                for character in self.unformat_characters:
                    captured_audio = captured_audio.replace(character, '')
            Utils.print_success("Whisper Speech Recognition thinks you said \"%s\" in %s" % (captured_audio, captured_language))
            self._analyse_audio(captured_audio)

        except sr.UnknownValueError:
            Utils.print_warning("Whisper Speech Recognition could not understand audio")
            # callback anyway, we need to listen again for a new order
            self._analyse_audio(audio_to_text=None)
        except sr.RequestError as e:
            Utils.print_danger("Could not request results from Whisper Speech Recognition service; {0}".format(e))
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