import sys

from core.NeuronModule import NeuronModule


class Kill_switch(NeuronModule):
    def __init__(self, **kwargs):
        super(Kill_switch, self).__init__(**kwargs)
        sys.exit()
