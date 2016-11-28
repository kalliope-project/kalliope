import time

from kalliope.core.NeuronModule import NeuronModule


class Systemdate(NeuronModule):
    def __init__(self, **kwargs):
        # get the cache if set by the user, if not, set it to false as it is not necessary
        cache = kwargs.get('cache', None)
        if cache is not None:
            kwargs["cache"] = cache
        else:
            kwargs["cache"] = False
        super(Systemdate, self).__init__(**kwargs)

        # local time and date
        hour = time.strftime("%H")          # Hour (24-hour clock) as a decimal number [00,23].
        minute = time.strftime("%M")        # Minute as a decimal number [00,59].
        weekday = time.strftime("%w")       # Weekday as a decimal number [0(Sunday),6].
        day_month = time.strftime("%d")     # Day of the month as a decimal number [01,31].
        month = time.strftime("%m")         # Month as a decimal number [01,12].
        year = time.strftime("%Y")          # Year with century as a decimal number. E.g: 2016

        self.message = {
            "hours": hour,
            "minutes": minute,
            "weekday": weekday,
            "month": month,
            "day_month": day_month,
            "year": year
        }
        
        self.say(self.message)
