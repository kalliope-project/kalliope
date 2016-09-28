class Event(object):
    def __init__(self, identifier, period):
        self.identifier = identifier
        self.period = period

    def __str__(self):
        return "%s: Id: %s, period: %s" % (self.__class__.__name__,
                                           self.identifier,
                                           self.period)
