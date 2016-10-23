import logging
import os
import subprocess

logging.basicConfig()
logger = logging.getLogger("kalliope")


MPLAYER_EXEC_PATH = "/usr/bin/mplayer"


class Mplayer(object):

    def __init__(self):
        mplayer_exec_path = [MPLAYER_EXEC_PATH]
        mplayer_options = ['-slave', '-quiet']
        self.mplayer_command = list()
        self.mplayer_command.extend(mplayer_exec_path)
        self.mplayer_command.extend(mplayer_options)

    def play(self, filepath):

        self.mplayer_command.append(filepath)
        logger.debug("Mplayer cmd: %s" % str(self.mplayer_command))

        FNULL = open(os.devnull, 'w')

        subprocess.call(self.mplayer_command, stdout=FNULL, stderr=FNULL)


