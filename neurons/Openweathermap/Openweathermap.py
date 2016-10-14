import pyowm

from core.NeuronModule import NeuronModule


class Openweathermap(NeuronModule):
    def __init__(self, **kwargs):
        # get message to spell out loud
        super(Openweathermap, self).__init__(**kwargs)

        api_key = kwargs.get('api_key', None)
        location = kwargs.get('location', None)
        lang = kwargs.get('lang', 'en')

        if api_key is None:
            raise NotImplementedError("OpenWeatherMap neuron needs an api_key")
        if location is None:
            raise NotImplementedError("OpenWeatherMap neuron needs a location")

        owm = pyowm.OWM(API_key=api_key, language=lang)

        forecast = owm.daily_forecast(location)
        tomorrow = pyowm.timeutils.tomorrow()
        weather_tomorrow = forecast.get_weather_at(tomorrow)
        weather_tomorrow_status = weather_tomorrow.get_detailed_status()

        observation = owm.weather_at_place(location)
        weather = observation.get_weather()
        weather_status = weather.get_detailed_status()

        print "weather :", weather_status
        print "weather_tomorrow :", weather_tomorrow_status

        message = {
            "location": location,
            "weather": weather_status,
            "weather_tomorrow":weather_tomorrow_status
        }

        self.say(message)


