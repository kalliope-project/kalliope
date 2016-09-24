import hashlib
import os
import shutil

import pygame
import requests
import logging
import sys

from core import AudioPlayer

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


def say(words=None, voice=None, language=VOXYGEN_LANGUAGES_DEFAULT, cache=True):
    voice = get_voice(voice, language)

    file_path = get_file_path(words, voice, language)

    if get_audio(voice, words, file_path, cache):
        AudioPlayer.play_audio(file_path, keep_file=cache)


def get_file_path(words, voice, language):
    md5 = hashlib.md5(words).hexdigest()
    filename = voice + "." + md5 + CACHE_EXTENSION
    cache_directory = os.path.join(CACHE_PATH, language)
    file_path = os.path.join(cache_directory, filename)
    create_directory(cache_directory)
    logging.debug("Cache directory %s exists and File path for audio is: %s", cache_directory, file_path)
    return file_path


def get_voice(voice, language):
    if language in VOXYGEN_LANGUAGES and voice in VOXYGEN_LANGUAGES[language]:
        return VOXYGEN_LANGUAGES[language][voice]

    logging.warn("Cannot find language matching language: %s voice: %s replace by default voice: %s", language, voice, VOXYGEN_VOICE_DEFAULT)
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
                return write_in_file(file_path, r.content)
            else:
                return False
        except IOError as e:
            logging.error("I/O error(%s): %s", e.errno, e.strerror)
        except ValueError:
            logging.error("Could not convert data to an integer.")
        except:
            logging.error("Unexpected error: %s", sys.exc_info()[0])
    else:
        return True


def write_in_file(file_path, content):
    with open(file_path, "wb") as file_open:
        file_open.write(content)
        file_open.close()
    return not file_is_empty(file_path)


def file_is_empty(file_path):
    return os.path.getsize(file_path) == 0


def create_directory(cache_path):
    if not os.path.exists(cache_path):
        os.makedirs(cache_path)


def wipe_cache():
    shutil.rmtree(CACHE_PATH)

