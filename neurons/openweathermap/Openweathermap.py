import pyowm

from core.NeuronModule import NeuronModule


class Openweathermap(NeuronModule):
    def __init__(self, **kwargs):
        # get message to spell out loud
        super(Openweathermap, self).__init__(**kwargs)

        self.api_key = kwargs.get('api_key', None)
        self.location = kwargs.get('location', None)
        self.lang = kwargs.get('lang', 'en')
        self.temp_unit = kwargs.get('temp_unit', 'celsius')
        self.country = kwargs.get('country', None)

        # check if parameters have been provided
        if self._is_parameters_ok():
            extended_location = self.location
            if self.country is not None:
                extended_location = self.location + "," + self.country


            owm = pyowm.OWM(API_key=self.api_key, language=self.lang)

            # Tomorrow
            forecast = owm.daily_forecast(extended_location)
            tomorrow = pyowm.timeutils.tomorrow()
            weather_tomorrow = forecast.get_weather_at(tomorrow)
            weather_tomorrow_status = weather_tomorrow.get_detailed_status()
            sunset_time_tomorrow = weather_tomorrow.get_sunset_time('iso')
            sunrise_time_tomorrow = weather_tomorrow.get_sunrise_time('iso')

            temp_tomorrow = weather_tomorrow.get_temperature(unit=self.temp_unit)
            temp_tomorrow_temp = temp_tomorrow['day']
            temp_tomorrow_temp_max = temp_tomorrow['max']
            temp_tomorrow_temp_min = temp_tomorrow['min']

            pressure_tomorrow = weather_tomorrow.get_pressure()
            pressure_tomorrow_press = pressure_tomorrow['press']
            pressure_tomorrow_sea_level = pressure_tomorrow['sea_level']

            humidity_tomorrow = weather_tomorrow.get_humidity()

            wind_tomorrow = weather_tomorrow.get_wind()
            # wind_tomorrow_deg = wind_tomorrow['deg']
            wind_tomorrow_speed = wind_tomorrow['speed']

            snow_tomorrow = weather_tomorrow.get_snow()
            rain_tomorrow = weather_tomorrow.get_rain()
            clouds_coverage_tomorrow = weather_tomorrow.get_clouds()

            # Today
            observation = owm.weather_at_place(extended_location)
            weather_today = observation.get_weather()
            weather_today_status = weather_today.get_detailed_status()
            sunset_time_today = weather_today.get_sunset_time('iso')
            sunrise_time_today = weather_today.get_sunrise_time('iso')

            temp_today = weather_today.get_temperature(unit=self.temp_unit)
            temp_today_temp = temp_today['temp']
            temp_today_temp_max = temp_today['temp_max']
            temp_today_temp_min = temp_today['temp_min']

            pressure_today = weather_today.get_pressure()
            pressure_today_press = pressure_today['press']
            pressure_today_sea_level = pressure_today['sea_level']

            humidity_today = weather_today.get_humidity()

            wind_today= weather_today.get_wind()
            wind_today_deg = wind_today['deg']
            wind_today_speed = wind_today['speed']

            snow_today = weather_today.get_snow()
            rain_today = weather_today.get_rain()
            clouds_coverage_today = weather_today.get_clouds()

            message = {
                "location": self.location,

                "weather_today": weather_today_status,
                "sunset_today_time": sunset_time_today,
                "sunrise_today_time": sunrise_time_today,
                "temp_today_temp": temp_today_temp,
                "temp_today_temp_max": temp_today_temp_max,
                "temp_today_temp_min": temp_today_temp_min,
                "pressure_today_press": pressure_today_press,
                "pressure_today_sea_level": pressure_today_sea_level,
                "humidity_today": humidity_today,
                "wind_today_deg": wind_today_deg,
                "wind_today_speed": wind_today_speed,
                "snow_today": snow_today,
                "rain_today": rain_today,
                "clouds_coverage_today": clouds_coverage_today,

                "weather_tomorrow": weather_tomorrow_status,
                "sunset_time_tomorrow": sunset_time_tomorrow,
                "sunrise_time_tomorrow": sunrise_time_tomorrow,
                "temp_tomorrow_temp": temp_tomorrow_temp,
                "temp_tomorrow_temp_max": temp_tomorrow_temp_max,
                "temp_tomorrow_temp_min": temp_tomorrow_temp_min,
                "pressure_tomorrow_press": pressure_tomorrow_press,
                "pressure_tomorrow_sea_level": pressure_tomorrow_sea_level,
                "humidity_tomorrow": humidity_tomorrow,
                # "wind_tomorrow_deg": wind_tomorrow_deg,
                "wind_tomorrow_speed": wind_tomorrow_speed,
                "snow_tomorrow": snow_tomorrow,
                "rain_tomorrow": rain_tomorrow,
                "clouds_coverage_tomorrow": clouds_coverage_tomorrow
            }

            self.say(message)

    def _is_parameters_ok(self):
        """
        Check if received parameters are ok to perform operations in the neuron
        :return: true if parameters are ok, raise an exception otherwise

        .. raises:: NotImplementedError
        """
        if self.api_key is None:
            raise NotImplementedError("OpenWeatherMap neuron needs an api_key")
        if self.location is None:
            raise NotImplementedError("OpenWeatherMap neuron needs a location")

        return True