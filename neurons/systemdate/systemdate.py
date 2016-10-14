#!/usr/bin/python
import time

from core.NeuronModule import NeuronModule


class Systemdate(NeuronModule):
    def __init__(self, **kwargs):
        super(Systemdate, self).__init__(**kwargs)

        # get hours and minutes

        hour = time.strftime("%H")
        minute = time.strftime("%M")


        message = {
            "hours": hour,
            "minutes": minute,
        }
        
        self.say(message)
