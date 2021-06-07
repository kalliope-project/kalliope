# coding: utf8
import logging
import os
import subprocess
import sndhdr

from kalliope.core.Utils.FileManager import FileManager

logging.basicConfig()
logger = logging.getLogger("kalliope")


class PlayerModule(object):
    """
    Mother class of Players. 
    Ability to convert sound files to wave format.
    """

    def __init__(self, **kwargs):

        # set parameter from what we receive from the settings
        self.convert = kwargs.get('convert_to_wav', True)

    @staticmethod
    def convert_mp3_to_wav(file_path_mp3):
        """
        API compatibility function as "mp3" is part of the method
        name, but the conversion via ffmpeg supports many other
        input formats as well. Please use convert_to_wav() instead.
        All invocations within kalliope haven been changed to call
        convert_to_wav(); this method invokes convert_to_wav() and
        remains only for compatiblity with plugins.
        :param file_path_mp3: the file path to convert to wav
        """
        return convert_to_wav(file_path=file_path_mp3)

    @staticmethod
    def convert_to_wav(file_path):
        """
        PyAudio, AlsaPlayer, sounddevices only support wav files.
        Other files must be converted to a wav in order to be played
        This function uses ffmpeg (which must be installed) for
        conversion; python core lib sndhdr is used to check if the
        provided file is already in wav format (skips conversion).
        :param file_path: the file path to convert to wav
        """
        filetype = sndhdr.whathdr(file_path)
        if filetype is None or filetype.filetype != 'wav':
            logger.debug("[PlayerModule] Converting file to wav file: %s" % file_path)
            fnull = open(os.devnull, 'w')
            # temp file
            tmp_file_wav = file_path+ ".wav"
            # Convert file to wave
            subprocess.call(['ffmpeg', '-y', '-i', file_path, tmp_file_wav],
                            stdout=fnull, stderr=fnull)
            # remove the original file
            FileManager.remove_file(file_path)
            # rename the temp file with the same name as the original file
            os.rename(tmp_file_wav, file_path)
