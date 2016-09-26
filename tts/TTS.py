from core import Cache


class TTS:
    def __init__(self):
        self.cache = Cache(module_name=self.__class__.__name__)
