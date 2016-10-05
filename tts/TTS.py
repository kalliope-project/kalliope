from core import AudioPlayer
from core import Cache


class TTS:
    def __init__(self, audio_player_type=None, cache_extension=None, volume=0.8):
        self.cache = Cache(module_name=self.__class__.__name__, cache_extension=cache_extension)
        self.audio_player = AudioPlayer(audio_player_type, volume=volume)

    def play_audio(self, music_file, cache=False):
        self.audio_player.play_audio(music_file)
        self.cache.remove_audio_file(music_file, cache)

    def unify_key(self, key):
        return key.lower()