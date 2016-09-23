import hashlib
import os
import shutil

import pygame
import requests
import logging

VOXYGEN_LANGUAGES = dict(
    fr=dict(electra="Electra", emma="Emma", becool="Becool", agnes="Agnes", loic="Loic", fabienne="Fabienne", helene="Helene", marion="Marion", matteo="Matteo",
            melodine="Melodine", mendoo="Mendoo", michel="Michel", moussa="Moussa", philippe="Philippe", sorciere="Sorciere"),
    ar=dict(adel="Adel"),
    de=dict(matthias="Matthias", jylvia="Sylvia"),
    uk=dict(bronwen="Bronwen", elizabeth="elizabeth", judith="Judith", paul="Paul", witch="Witch"),
    us=dict(bruce="Bruce", jenny="Jenny"),
    es=dict(martha="Martha"),
    it=dict(sonia="Sonia"))

VOXYGEN_LANGUAGE_DEFAULT = "Michel"
VOXYGEN_URL = "https://www.voxygen.fr/sites/all/modules/voxygen_voices/assets/proxy/index.php"

CACHE_PATH = "/tmp/jarvis/tts/voxygen"
CACHE_EXTENSION = ".tts"
AUDIO_FREQUENCY = 16000
AUDIO_SIZE = -16
AUDIO_CHANNEL = 1
AUDIO_BUFFER = 2048


def say(words=None, voice=None, language=None, cache=None):
    create_directory()

    voice = get_voice(voice, language)

    file_path = get_file_path(words,voice,language)

    get_audio(voice, words, file_path, cache)

    play_audio(file_path)

    remove_temp_file(file_path, cache)


def get_file_path(words, voice, language):
    sha1 = hashlib.sha1(words).hexdigest()
    filename = voice + "." + sha1 + CACHE_EXTENSION
    file_path = os.path.join(CACHE_PATH, filename)
    return file_path


def get_voice(voice=None, language=None):
    if language in VOXYGEN_LANGUAGES:
        if voice in VOXYGEN_LANGUAGES[language]:
            return VOXYGEN_LANGUAGES[language][voice]

    logging.debug("Cannot find language matching language: %s voice: %s replace by default voice: %s", language, voice, VOXYGEN_LANGUAGE_DEFAULT)
    return VOXYGEN_LANGUAGE_DEFAULT


def get_audio(voice, text, file_path, cache):
    if not cache or not os.path.exists(file_path):
        payload = {
            "method": "redirect",
            "text": text.encode('utf8'),
            "voice": voice
        }

        r = requests.get(VOXYGEN_URL, params=payload, stream=True)
        logging.debug("Trying to get url: %s response code: %s", r.url, r.status_code)

        try:
            if r.status_code == 200:
                with open(file_path, "w") as sound_file:
                    sound_file.write(r.content)
        except IOError as e:
            print("I/O error({0}): {1}".format(e.errno, e.strerror))
        except ValueError:
            print("Could not convert data to an integer.")
        except:
            print("Unexpected error:", sys.exc_info()[0])


def play_audio(music_file, volume=0.8):
    pygame.mixer.init(AUDIO_FREQUENCY, AUDIO_SIZE, AUDIO_CHANNEL, AUDIO_BUFFER)
    pygame.mixer.music.set_volume(volume)
    clock = pygame.time.Clock()
    try:
        pygame.mixer.music.load(music_file)
        logging.debug("Music file %s loaded!", music_file)
    except pygame.error:
        remove_file(music_file)
        logging.debug("File %s not found! (%s)",music_file, pygame.get_error())
        return
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        clock.tick(10)


def remove_temp_file(file_path, cache):
    if not cache:
        remove_file(file_path)


def remove_file(path):
    if os.path.exists(path):
        os.remove(path)


def create_directory():
    if not os.path.exists(CACHE_PATH):
        os.makedirs(CACHE_PATH)


def wipe_cache():
    shutil.rmtree(CACHE_PATH)

