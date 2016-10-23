import logging
import os
import subprocess

logging.basicConfig()
logger = logging.getLogger("kalliope")


MPLAYER_EXEC_PATH = "/usr/bin/mplayer"


class Mplayer(object):

    def __init__(self):
        pass

    @classmethod
    def play(cls, filepath):
        mplayer_exec_path = [MPLAYER_EXEC_PATH]
        mplayer_options = ['-slave', '-quiet']
        mplayer_command = list()
        mplayer_command.extend(mplayer_exec_path)
        mplayer_command.extend(mplayer_options)

        mplayer_command.append(filepath)
        logger.debug("Mplayer cmd: %s" % str(mplayer_command))

        FNULL = open(os.devnull, 'w')

        subprocess.call(mplayer_command, stdout=FNULL, stderr=FNULL)


