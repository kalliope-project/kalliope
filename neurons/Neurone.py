import importlib


class Neurone:
    def __init__(self, stt=None, tts=None):
        # TODO load the stt and tts from settings
        self.stt = "snowboy"
        self.tts = "pico2wave"

    def say(self, message):
        # here we use the tts to make jarvis talk
        # the module is imported on fly, depending on the selected tts from settings
        tts_backend = importlib.import_module("tts." + self.tts)
        tts_backend.say(message)

