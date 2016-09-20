#!/usr/bin/python
import time

from neurons import Neurone


class Systemdate(Neurone):
    def __init__(self):
        Neurone.__init__(self)
        hour = time.strftime("%H")
        minute = time.strftime("%M")
        message = "Il est %s heure %s" % (hour, minute)
        self.say(message)
