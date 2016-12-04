class Event(object):
    """
    This Class is representing an Event which is raised by when the System at some defined time.

    .. note:: Events are based on the system crontab
    """

    def __init__(self, year=None, month=None, day=None, week=None, day_of_week=None,
                 hour=None, minute=None, second=None):
        self.year = year
        self.month = month
        self.day = day
        self.week = week
        self.day_of_week = day_of_week
        self.hour = hour
        self.minute = minute
        self.second = second

    def __str__(self):
        return "%s:  year: %s, month: %s, day: %s, week: %s, day_of_week: %s, hour: %s, minute: %s, second: %s" \
               % (self.__class__.__name__, self.year, self.month, self.day, self.week,
                  self.day_of_week, self.hour, self.minute, self.second)

    def serialize(self):
        """
        This method allows to serialize in a proper way this object

        :return: A dict of name / period
        :rtype: Dict
        """

        return {
            'event': {
                "year": self.year,
                "month": self.month,
                "day": self.day,
                "week": self.week,
                "day_of_week": self.day_of_week,
                "hour": self.hour,
                "minute": self.minute,
                "second": self.second,
            }
        }

    def __eq__(self, other):
        """
        This is used to compare 2 objects
        :param other:
        :return:
        """
        return self.__dict__ == other.__dict__
