import subprocess

from neurons import Neurone


class Command(Neurone):
    def __init__(self, command):
        Neurone.__init__(self)
        p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()


