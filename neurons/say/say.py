from neurons import Neurone


class NoMessageException(Exception):
    pass


class Say(Neurone):
    def __init__(self, *args, **kwargs):
        Neurone.__init__(self, **kwargs)
        # get message to spell out loud
        message = kwargs.get('message', None)
        # user must specify a message
        if message is None:
            raise NoMessageException("You must specify a message string or a list of messages as parameter")
        else:
            self.say(message, kwargs)
