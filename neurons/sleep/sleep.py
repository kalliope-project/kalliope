import time

from core.NeuronModule import NeuronModule


class NoSecondsException(Exception):
    pass


class Sleep(NeuronModule):

    def __init__(self, **kwargs):
        # get message to spell out loud
        super(Sleep, self).__init__(**kwargs)
        seconds = kwargs.get('seconds', None)
        # user must specify a message
        if seconds is None:
            raise NoSecondsException("You must set a number of seconds as parameter")
        time.sleep(seconds)



