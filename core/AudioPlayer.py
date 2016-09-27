import logging
import pygame

from core.FileManager import FileManager


class AudioPlayer:
    PLAYER_MP3 = "MP3"
    PLAYER_WAV = "WAV"

    AUDIO_MP3_FREQUENCY = 16000
    AUDIO_MP3_SIZE = -16
    AUDIO_MP3_CHANNEL = 1
    AUDIO_MP3_BUFFER = 2048

    AUDIO_DEFAULT_VOLUME = 0.8

    def __init__(self, default_type=None, audio_frequency=AUDIO_MP3_FREQUENCY, audio_size=AUDIO_MP3_SIZE, audio_channel=AUDIO_MP3_CHANNEL, audio_buffer=AUDIO_MP3_BUFFER, volume=AUDIO_DEFAULT_VOLUME):
        if default_type == self.PLAYER_MP3:
            self.audio_frequency = self.AUDIO_MP3_FREQUENCY
            self.audio_size = self.AUDIO_MP3_SIZE
            self.audio_channel = self.AUDIO_MP3_CHANNEL
            self.audio_buffer = self.AUDIO_MP3_BUFFER
        else:
            self.audio_frequency = audio_frequency
            self.audio_size = audio_size
            self.audio_channel = audio_channel
            self.audio_buffer = audio_buffer
        self.volume = volume
        pygame.mixer.init(audio_frequency, audio_size, audio_channel, audio_buffer)

    def play_audio(self, music_file):
        try:
            self._init_player_audio(music_file)
            logging.debug("Music file %s loaded!", music_file)
        except pygame.error:
            FileManager.remove_file(music_file)
            logging.error("File %s not found! (%s)", music_file, pygame.get_error())
            return

        self._start_player_audio()

    def _init_player_audio(self, music_file):
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.load(music_file)

    @staticmethod
    def _start_player_audio():
        logging.info("Starting pygame audio player")
        pygame.mixer.music.play()
        clock = pygame.time.Clock()
        while pygame.mixer.music.get_busy():
            clock.tick(20)
        return
