import pyowm

from core.NeuronModule import NeuronModule


class OpenWeatherMap(NeuronModule):
    def __init__(self, **kwargs):
        # get message to spell out loud
        super(OpenWeatherMap, self).__init__(**kwargs)

        api_key = kwargs.get('api_key', None)
        location = kwargs.get('location', None)
        date = kwargs.get('date', None)

        if api_key is None:
            raise NotImplementedError("OpenWeatherMap neuron needs an api_key")
        if location is None:
            raise NotImplementedError("OpenWeatherMap neuron needs a location")

        owm = pyowm.OWM(api_key)


        # forecast = owm.daily_forecast(location)
        # tomorrow = pyowm.timeutils.tomorrow()
        # forecast.will_be_sunny_at(tomorrow)

        observation = owm.weather_at_place(location)
        weather = observation.get_weather()

        message = {
            "date": date,
            "weathers": weather,
        }

        self.say(message)


