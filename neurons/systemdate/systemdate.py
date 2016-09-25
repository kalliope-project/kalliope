#!/usr/bin/python
import time

from neurons import Neurone


class Systemdate(Neurone):
    def __init__(self, *args , **kwargs):
        Neurone.__init__(self, **kwargs)
        hour = time.strftime("%H")
        minute = time.strftime("%M")

        message = {
            "hours":hour,
            "minutes":minute
        }
        self.say(message, kwargs)
