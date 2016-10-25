class Event(object):
    def __init__(self, period):
        self.period = period

    def __str__(self):
        return "%s: period: %s" % (self.__class__.__name__,
                                   self.period)

    def serialize(self):
        return {
            'event': self.period
        }
