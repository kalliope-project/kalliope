import logging
import os
import subprocess

logging.basicConfig()
logger = logging.getLogger("kalliope")

MPLAYER_EXEC_PATH = "/usr/bin/mplayer"


class Mplayer(object):
    """
    This Class is representing the MPlayer Object used to play the all sound of the system.
    """

    def __init__(self):
        pass

    @classmethod
    def play(cls, filepath):
        """
        Play the sound located in the provided filepath

        :param filepath: The file path of the sound to play
        :type filepath: str

        :Example:

            Mplayer.play(self.file_path)

        .. seealso::  TTS
        .. raises::
        .. warnings:: Class Method and Public
        """

        mplayer_exec_path = [MPLAYER_EXEC_PATH]
        mplayer_options = ['-slave', '-quiet']
        mplayer_command = list()
        mplayer_command.extend(mplayer_exec_path)
        mplayer_command.extend(mplayer_options)

        mplayer_command.append(filepath)
        logger.debug("Mplayer cmd: %s" % str(mplayer_command))

        fnull = open(os.devnull, 'w')

        subprocess.call(mplayer_command, stdout=fnull, stderr=fnull)
