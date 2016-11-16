class Event(object):
    """
    This Class is representing an Event which is raised by when the System at some defined time.

    .. note:: Events are based on the system crontab
    """

    def __init__(self, period):
        self.period = period

    def __str__(self):
        return "%s: period: %s" % (self.__class__.__name__,
                                   self.period)

    def serialize(self):
        """
        This method allows to serialize in a proper way this object

        :return: A dict of name / period
        :rtype: Dict
        """

        return {
            'event': self.period
        }

    def __eq__(self, other):
        """
        This is used to compare 2 objects
        :param other:
        :return:
        """
        return self.__dict__ == other.__dict__
