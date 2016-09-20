from neurons import Neurone


class Say(Neurone):
    def __init__(self, *args , **kwargs):
        Neurone.__init__(self)

        # get message to spell out loud
        message = kwargs.get('message', "")
        self.say(message)
