#!/usr/bin/python
import time

from core.Models.Neurone import Neurone


class Systemdate(Neurone):
    def __init__(self, **kwargs):
        Neurone.__init__(self, **kwargs)

        # get hours and minutes
        hour = time.strftime("%H")
        minute = time.strftime("%M")

        message = {
            "hours": hour,
            "minutes": minute
        }
        self.say(message, **kwargs)
