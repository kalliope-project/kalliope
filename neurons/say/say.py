from neurons import Neurone
import random


class NoMessageException(Exception):
    pass


class Say(Neurone):
    def __init__(self, *args , **kwargs):
        # get the tts if is specified
        tts = kwargs.get('tts', None)
        Neurone.__init__(self, tts=tts)

        # get message to spell out loud
        message = kwargs.get('message', None)
        # user must specify a message
        if message is None:
            raise NoMessageException("You must specify a message string or a list of messages as parameter")
        else:
            # check if it's a single message or multiple one
            if isinstance(message, list):
                # then we play randomly one message
                self.say(random.choice(message))
            else:
                self.say(message)
