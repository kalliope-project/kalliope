#!/usr/bin/python
import time
from core import Neurone


class SystemDate(Neurone):
    def __init__(self):
        Neurone.__init__(self)
        date_now = time.strftime("%H:%M")
        self.say(date_now)
