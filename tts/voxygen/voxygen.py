import sha
import os

import pygame
import requests

VOXYGEN_LANGUAGES = {
    "fr" : {"electra":"Electra","emma":"Emma","becool":"Becool","agnes":"Agnes","loic":"Loic","fabienne":"Fabienne","helene":"Helene","marion":"Marion","matteo":"Matteo","melodine":"Melodine","mendoo":"Mendoo","michel":"Michel","moussa":"Moussa","philippe":"Philippe","sorciere":"Sorciere"},
    "ar" : {"adel":"Adel"},
    "de" : {"matthias":"Matthias","jylvia":"Sylvia"},
    "uk" : {"bronwen":"Bronwen","elizabeth":"elizabeth","judith":"Judith","paul":"Paul","witch":"Witch"},
    "us" : {"bruce":"Bruce","jenny":"Jenny"},
    "es" : {"martha":"Martha"},
    "it" : {"sonia":"Sonia"}
}

def say(words=None, voice=None, language=None, cache=None):
    path = "/tmp/jarvis/tts/voxygen/"
    if not os.path.exists(path):
        os.makedirs(path)

    sha1 = sha.new(words).hexdigest()

    tempfile = path+voice+"."+sha1+".tts"

    get_audio(voice,words,tempfile,cache)

    play_audio(tempfile)

    if not cache:
        os.remove(tempfile)

def get_audio(voice, text, filepath,cache):
    if not cache or not os.path.exists(filepath):
        payload ={
            "method" : "redirect",
            "text" : text.encode('utf8'),
            "voice" : voice
        }

        r = requests.get("https://www.voxygen.fr/sites/all/modules/voxygen_voices/assets/proxy/index.php", params=payload, stream=True)
        logging.debug("Trying to get url: %s response code: %s",r.url,r.status_code)

        if r.status_code==200:
            with open(os.path.abspath(filepath), "wb") as sound_file:
                sound_file.write(r.content)

def play_audio(music_file, volume=0.8):
    pygame.mixer.init(16000, -16, 1, 2048)
    pygame.mixer.music.set_volume(volume)
    clock = pygame.time.Clock()
    try:
        pygame.mixer.music.load(music_file)
        logging.debug("Music file {} loaded!".format(music_file))
    except pygame.error:
        os.remove(music_file)
        logging.debug("File {} not found! ({})".format(music_file, pygame.get_error()))
        return
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        clock.tick(10)

def get_voice(voice=None, language=None):
    if language in VOXYGEN_LANGUAGES:
        if voice in VOXYGEN_LANGUAGES[language]:
            return VOXYGEN_LANGUAGES[language][voice]

    logging.debug("Cannot find language maching language: %s voice: %s",language,voice)
    return ""