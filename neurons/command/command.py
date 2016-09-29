import subprocess

from core.NeuronModule import NeuronModule


class Command(NeuronModule):
    def __init__(self, command, **kwargs):
        super(Command, self).__init__(**kwargs)
        p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()


