from core.NeuronModule import NeuronModule


class NoMessageException(Exception):
    pass


class Say(NeuronModule):
    def __init__(self, **kwargs):
        super(Say, self).__init__(**kwargs)
        # get message to spell out loud
        message = kwargs.get('message', None)
        # user must specify a message
        if message is None:
            raise NoMessageException("You must specify a message string or a list of messages as parameter")
        else:
            self.say(message)
