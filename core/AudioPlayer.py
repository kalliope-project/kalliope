import logging
import pygame

from core.FileManager import FileManager

logging.basicConfig()
logger = logging.getLogger("kalliope")


class AudioPlayer:
    PLAYER_MP3 = "mp3"
    PLAYER_WAV = "wav"

    AUDIO_MP3_FREQUENCY = 16000
    AUDIO_MP3_SIZE = -16
    AUDIO_MP3_CHANNEL = 1
    AUDIO_MP3_BUFFER = 2048

    AUDIO_MP3_44100_FREQUENCY = 44100
    AUDIO_MP3_22050_FREQUENCY = 22050

    AUDIO_DEFAULT_VOLUME = 0.8

    def __init__(self, volume=AUDIO_DEFAULT_VOLUME):
        self.volume = volume

    def init_play(self, default_type=None, audio_frequency=AUDIO_MP3_FREQUENCY, audio_size=AUDIO_MP3_SIZE, audio_channel=AUDIO_MP3_CHANNEL,
                  audio_buffer=AUDIO_MP3_BUFFER):
        if default_type == self.PLAYER_MP3 or default_type == self.PLAYER_MP3:
            audio_size = self.AUDIO_MP3_SIZE
            audio_channel = self.AUDIO_MP3_CHANNEL
            audio_buffer = self.AUDIO_MP3_BUFFER
        else:
            audio_size = audio_size
            audio_channel = audio_channel
            audio_buffer = audio_buffer

        audio_frequency = audio_frequency
        pygame.mixer.pre_init(audio_frequency, audio_size, audio_channel, audio_buffer)
        pygame.mixer.init()

    def play_audio(self, music_file):
        try:
            self._init_player_audio(music_file)
            logger.debug("Music file %s loaded!", music_file)
        except pygame.error:
            FileManager.remove_file(music_file)
            logger.error("File %s not found! (%s)", music_file, pygame.get_error())
            return

        self._start_player_audio()

    def _init_player_audio(self, music_file):
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.load(music_file)

    @staticmethod
    def _start_player_audio():
        clock = pygame.time.Clock()
        clock.tick(100)
        logger.debug("Starting pygame audio player")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            clock.tick(20)
        pygame.mixer.quit()
        return
