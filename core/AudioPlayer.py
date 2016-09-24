import logging
import pygame
import os


class AudioPlayer:
    AUDIO_FREQUENCY = 16000
    AUDIO_SIZE = -16
    AUDIO_CHANNEL = 1
    AUDIO_BUFFER = 2048

    @classmethod
    def play_audio(cls, music_file, volume=0.8, keep_file=False):
        try:
            cls._init_player_audio(music_file, volume)
            logging.debug("Music file %s loaded!", music_file)
        except pygame.error:
            cls._remove_file(music_file)
            logging.error("File %s not found! (%s)", music_file, pygame.get_error())
            return

        cls._start_player_audio()
        if not keep_file:
            cls._remove_file(music_file)

    @classmethod
    def _init_player_audio(cls, music_file, volume):
        pygame.mixer.init(cls.AUDIO_FREQUENCY, cls.AUDIO_SIZE, cls.AUDIO_CHANNEL, cls.AUDIO_BUFFER)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.load(music_file)

    @staticmethod
    def _start_player_audio():
        logging.info("Starting pygame audio player")
        pygame.mixer.music.play()
        clock = pygame.time.Clock()
        while pygame.mixer.music.get_busy():
            clock.tick(10)
        return

    @staticmethod
    def _remove_file(file_path):
        if os.path.exists(file_path):
            return os.remove(file_path)
