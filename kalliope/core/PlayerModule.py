# coding: utf8
import logging
import os
import subprocess

from kalliope.core.Utils.FileManager import FileManager

logging.basicConfig()
logger = logging.getLogger("kalliope")


class PlayerModule(object):
    """
    Mother class of Players. 
    Ability to convert mp3 to wave format.
    """

    def __init__(self, **kwargs):

        # set parameter from what we receive from the settings
        self.convert = kwargs.get('convert_to_wav', True)

    @staticmethod
    def convert_mp3_to_wav(file_path_mp3):
        """ 
        PyAudio, AlsaPlayer, sounddevices  do not support mp3 files 
        MP3 files must be converted to a wave in order to be played
        This function assumes ffmpeg is available on the system
        :param file_path_mp3: the file path to convert from mp3 to wav
        """
        logger.debug("[PlayerModule] Converting mp3 file to wav file: %s" % file_path_mp3)
        fnull = open(os.devnull, 'w')
        # temp file
        tmp_file_wav = file_path_mp3 + ".wav"
        # Convert mp3 to wave
        subprocess.call(['ffmpeg', '-y', '-i', file_path_mp3, tmp_file_wav],
                        stdout=fnull, stderr=fnull)
        # remove the original file
        FileManager.remove_file(file_path_mp3)
        # rename the temp file with the same name as the original file
        os.rename(tmp_file_wav, file_path_mp3)