from core import AudioPlayer
from core import Cache


class TTS:
    def __init__(self, audio_player_type=None):
        self.cache = Cache(module_name=self.__class__.__name__)
        self.audio_player = AudioPlayer(audio_player_type)

    def play_audio(self, music_file, volume=0.8, keep_file=False):
        self.audio_player.play_audio(music_file, volume, keep_file)
