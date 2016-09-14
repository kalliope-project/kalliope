from core import Neurone


class Say(Neurone):
    def __init__(self, message):
        Neurone.__init__(self)
        self.say(message)
