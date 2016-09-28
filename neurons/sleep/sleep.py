import time

from core.Models.Neurone import Neurone


class NoSecondsException(Exception):
    pass


class Sleep(Neurone):

    def __init__(self, *args , **kwargs):
        Neurone.__init__(self)

        # get message to spell out loud
        seconds = kwargs.get('seconds', None)
        # user must specify a message
        if seconds is None:
            raise NoSecondsException("You must set a number of seconds as parameter")
        time.sleep(seconds)



