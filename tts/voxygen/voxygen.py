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

VOXYGEN_VOICE_DEFAULT = "Michel"
VOXYGEN_LANGUAGES_DEFAULT = "default"
VOXYGEN_URL = "https://www.voxygen.fr/sites/all/modules/voxygen_voices/assets/proxy/index.php"
VOXYGEN_CONTENT_TYPE = "audio/mpeg"
VOXYGEN_TIMEOUT_SEC = 30

CACHE_PATH = "/tmp/jarvis/tts/voxygen"
CACHE_EXTENSION = ".tts"

AUDIO_FREQUENCY = 16000
AUDIO_SIZE = -16
AUDIO_CHANNEL = 1
AUDIO_BUFFER = 2048


def say(words=None, voice=None, language=VOXYGEN_LANGUAGES_DEFAULT, cache=None):
    voice = get_voice(voice, language)

    file_path = get_file_path(words, voice, language)

    if get_audio(voice, words, file_path, cache):
        play_audio(file_path)
        remove_temp_file(file_path, cache)


def get_file_path(words, voice, language):
    sha1 = hashlib.sha1(words).hexdigest()
    filename = voice + "." + sha1 + CACHE_EXTENSION
    cache_directory = os.path.join(CACHE_PATH, language)
    file_path = os.path.join(cache_directory, filename)
    create_directory(cache_directory)
    logging.debug("Cache directory %s exists and File path for audio is: %s", cache_directory, file_path)
    return file_path


def get_voice(voice, language):
    if language in VOXYGEN_LANGUAGES and voice in VOXYGEN_LANGUAGES[language]:
        return VOXYGEN_LANGUAGES[language][voice]

    logging.debug("Cannot find language matching language: %s voice: %s replace by default voice: %s", language, voice, VOXYGEN_VOICE_DEFAULT)
    return VOXYGEN_VOICE_DEFAULT


def get_audio(voice, text, file_path, cache):
    if not cache or not os.path.exists(file_path) or file_is_empty(file_path):
        payload = {
            "method": "redirect",
            "text": text.encode('utf8'),
            "voice": voice
        }

        r = requests.get(VOXYGEN_URL, params=payload, stream=True, timeout=VOXYGEN_TIMEOUT_SEC)

        content_type = r.headers['Content-Type']
        logging.debug("Trying to get url: %s response code: %s and content-type: %s", r.url, r.status_code, content_type)

        try:
            if r.status_code == requests.codes.ok and content_type == VOXYGEN_CONTENT_TYPE:
                write_in_file(file_path, r.content)
                return True
            else:
                return False
        except IOError as e:
            print("I/O error(%s): %s", e.errno, e.strerror)
        except ValueError:
            print("Could not convert data to an integer.")
        except:
            print("Unexpected error: %s", sys.exc_info()[0])
    else:
        return True


def play_audio(music_file, volume=0.8):
    try:
        init_player_audio(music_file, volume)
        logging.debug("Music file %s loaded!", music_file)
    except pygame.error:
        remove_file(music_file)
        logging.debug("File %s not found! (%s)", music_file, pygame.get_error())
        return

    start_player_audio()


def init_player_audio(music_file, volume):
    pygame.mixer.init(AUDIO_FREQUENCY, AUDIO_SIZE, AUDIO_CHANNEL, AUDIO_BUFFER)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.load(music_file)


def start_player_audio():
    pygame.mixer.music.play()
    clock = pygame.time.Clock()
    while pygame.mixer.music.get_busy():
        clock.tick(10)
    return


def remove_temp_file(file_path, cache):
    if not cache:
        remove_file(file_path)


def remove_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)


def write_in_file(file_path, content):
    with open(file_path, "wb") as file_open:
        file_open.write(content)
        file_open.close()


def file_is_empty(file_path):
    return os.path.getsize(file_path) == 0


def create_directory(cache_path):
    if not os.path.exists(cache_path):
        os.makedirs(cache_path)


def wipe_cache():
    shutil.rmtree(CACHE_PATH)

