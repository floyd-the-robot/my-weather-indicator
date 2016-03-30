#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#
# A library for access to google weather api
#
# Copyright (C) 2011 Lorenzo Carbonell
# lorenzo.carbonell.cerezo@gmail.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
import weatherservice
import geocodeapi
from weatherservice import WeatherService
import yql
from comun import _
from comun import read_from_url

API_KEY = 'dj0yJmk9djNkNk5hRUZNODFCJmQ9WVdrOWVEbFVXRWxITTJVbWNHbzlNQS0tJnM9Y29uc3VtZXJzZW\
NyZXQmeD1jMQ--'
SHARED_SECRET = '27dcb39434d1ee95b90e5f3a7e227d3992ecd573'

ID = '_slN0oHV34Exg09kl5EASmbGBs5y3GJES1N.Oon0wd5Lnh6E5hGdtQmx_MdxpOxKAzf\
tS1dB0yNI_NzTpWaKFXEm'
YAHOO_WOEID_URL = 'http://where.yahooapis.com/geocode?q=%s,+%s&gflags=R&\
appid=%s'
YAHOO_WEATHER_URL = 'http://weather.yahooapis.com/forecastrss?w=%s&u=f'
WEATHER_NS = 'http://xml.weather.yahoo.com/ns/rss/1.0'

CODE = {}
CODE[0] = 'tornado'
CODE[1] = 'tropical storm'
CODE[2] = 'hurricane'
CODE[3] = 'severe thunderstorms'
CODE[4] = 'thunderstorms'
CODE[5] = 'mixed rain and snow'
CODE[6] = 'mixed rain and sleet'
CODE[7] = 'mixed snow and sleet'
CODE[8] = 'freezing drizzle'
CODE[9] = 'drizzle'
CODE[10] = 'freezing rain'
CODE[11] = 'showers'
CODE[12] = 'showers'
CODE[13] = 'snow flurries'
CODE[14] = 'light snow showers'
CODE[15] = 'blowing snow'
CODE[16] = 'snow'
CODE[17] = 'hail'
CODE[18] = 'sleet'
CODE[19] = 'dust'
CODE[20] = 'foggy'
CODE[21] = 'haze'
CODE[22] = 'smoky'
CODE[23] = 'blustery'
CODE[24] = 'windy'
CODE[25] = 'cold'
CODE[26] = 'cloudy'
CODE[27] = 'mostly cloudy'
CODE[28] = 'mostly cloudy'
CODE[29] = 'partly cloudy'
CODE[30] = 'partly cloudy'
CODE[31] = 'clear'
CODE[32] = 'sunny'
CODE[33] = 'fair'
CODE[34] = 'fair'
CODE[35] = 'mixed rain and hail'
CODE[36] = 'hot'
CODE[37] = 'isolated thunderstorms'
CODE[38] = 'scattered thunderstorms'
CODE[39] = 'scattered thunderstorms'
CODE[40] = 'scattered showers'
CODE[41] = 'heavy snow'
CODE[42] = 'scattered snow showers'
CODE[43] = 'heavy snow'
CODE[44] = 'partly cloudy'
CODE[45] = 'thundershowers'
CODE[46] = 'snow showers'
CODE[47] = 'isolated thundershowers'
CODE[3200] = 'not available'


class YahooWeatherService(WeatherService):

    def __init__(self,
                 longitude=-0.418,
                 latitude=39.360,
                 units=weatherservice.Units()):
        WeatherService.__init__(self, longitude, latitude, units)
        gw = geocodeapi.get_inv_direction(latitude, longitude)
        if gw is None:
            self.woeid = None
            self.y = None
        else:
            self.woeid = geocodeapi.get_inv_direction(latitude,
                                                      longitude)['woeid']
            self.y = yql.TwoLegged(API_KEY, SHARED_SECRET)

    def get_weather(self):
        weather_data = self.get_default_values()
        if self.woeid is None:
            print('Yahoo Weather Service, not found woeid')
            return
        print('-------------------------------------------------------')
        print('-------------------------------------------------------')
        print('Yahoo Weather Service woeid: %s' % self.woeid)
        print('-------------------------------------------------------')
        print('-------------------------------------------------------')
        try:
            query = 'select * from weather.forecast where woeid="%s"' % \
                (self.woeid)
            ans = self.y.execute(query)
            print('************************************************')
            print(query)
            print(ans.results)
            print('************************************************')
            readed = read_from_url(self.url).decode()
            wind_conditions = get_wind_conditions(readed)
            atmosphere_conditions = get_atmosphere_conditions(readed)
            current_conditions = get_current_conditions(readed)
            forecast_conditions = get_forecast_conditions(readed)
            current_location = get_location(readed)
            temperature = current_conditions[1]
            velocity = wind_conditions[1]
            direction = wind_conditions[0]
            pressure = atmosphere_conditions[2]/0.0294985250737
            visibility = atmosphere_conditions[1]
            humidity = atmosphere_conditions[0]
            condition = current_conditions[0]
            weather_data['current_conditions']['condition'] = condition
            weather_data['current_conditions']['condition_text'] =\
                weatherservice.get_condition(condition, 'text')
            if weather_data['current_conditions']['isday']:
                weather_data['current_conditions']['condition_image'] =\
                    weatherservice.get_condition(condition, 'image')
                weather_data['current_conditions']['condition_icon_dark'] =\
                    weatherservice.get_condition(condition, 'icon-dark')
                weather_data['current_conditions']['condition_icon_light'] =\
                    weatherservice.get_condition(condition, 'icon-light')
            else:
                weather_data['current_conditions']['condition_image'] =\
                    weatherservice.get_condition(condition, 'image-night')
                weather_data['current_conditions']['condition_icon_dark'] =\
                    weatherservice.get_condition(condition, 'icon-night-dark')
                weather_data['current_conditions']['condition_icon_light'] =\
                    weatherservice.get_condition(condition, 'icon-night-light')
            weather_data['current_conditions']['temperature'] =\
                weatherservice.change_temperature(temperature,
                                                  self.units.temperature)
            weather_data['current_conditions']['pressure'] =\
                weatherservice.change_pressure(pressure, self.units.pressure)
            weather_data['current_conditions']['humidity'] = '%s %%' %\
                (humidity)
            weather_data['current_conditions']['dew_point'] =\
                weatherservice.get_dew_point(humidity,
                                             temperature,
                                             self.units.temperature)
            wind_direction = weatherservice.degToCompass2(direction)
            weather_data['current_conditions']['wind_condition'] =\
                weatherservice.get_wind_condition2(velocity,
                                                   wind_direction[0],
                                                   self.units.wind)
            weather_data['current_conditions']['wind_icon'] = wind_direction[2]
            #
            weather_data['current_conditions']['heat_index'] =\
                weatherservice.get_heat_index(temperature, humidity)
            weather_data['current_conditions']['windchill'] =\
                weatherservice.get_wind_chill(temperature, velocity)
            #
            weather_data['current_conditions']['feels_like'] =\
                weatherservice.get_feels_like(temperature,
                                              humidity,
                                              velocity,
                                              self.units.temperature)
            #
            weather_data['current_conditions']['visibility'] =\
                weatherservice.change_distance(visibility,
                                               self.units.visibility)
            weather_data['current_conditions']['solarradiation'] = None
            weather_data['current_conditions']['UV'] = None
            weather_data['current_conditions']['precip_1hr'] = None
            weather_data['current_conditions']['precip_today'] = None
            for i, forecast_condition in enumerate(forecast_conditions):
                t1 = weatherservice.s2f(forecast_condition[1])
                t2 = weatherservice.s2f(forecast_condition[2])
                if t1 < t2:
                    tmin = str(t1)
                    tmax = str(t2)
                else:
                    tmin = str(t2)
                    tmax = str(t1)
                weather_data['forecasts'][i]['low'] =\
                    weatherservice.change_temperature(tmin,
                                                      self.units.temperature)
                weather_data['forecasts'][i]['high'] =\
                    weatherservice.change_temperature(tmax,
                                                      self.units.temperature)
                #
                weather_data['forecasts'][i]['qpf_allday'] = None
                weather_data['forecasts'][i]['qpf_day'] = None
                weather_data['forecasts'][i]['qpf_night'] = None
                weather_data['forecasts'][i]['snow_allday'] = None
                weather_data['forecasts'][i]['snow_day'] = None
                weather_data['forecasts'][i]['snow_night'] = None
                weather_data['forecasts'][i]['maxwind'] = None
                weather_data['forecasts'][i]['avewind'] = None
                weather_data['forecasts'][i]['avehumidity'] = None
                weather_data['forecasts'][i]['maxhumidity'] = None
                weather_data['forecasts'][i]['minhumidity'] = None
                #
                weather_data['forecasts'][i]['condition'] =\
                    forecast_condition[0]
                weather_data['forecasts'][i]['condition_text'] =\
                    weatherservice.get_condition(forecast_condition[0],
                                                 'text')
                weather_data['forecasts'][i]['condition_image'] =\
                    weatherservice.get_condition(forecast_condition[0],
                                                 'image')
                weather_data['forecasts'][i]['condition_icon'] =\
                    weatherservice.get_condition(forecast_condition[0],
                                                 'icon-light')
        except Exception as e:
            print(e)
        return weather_data

if __name__ == "__main__":
    longitude = -0.418
    latitude = 39.360
    # latitude, longitude = 44.434295, 26.102965
    # latitude ,longitude = 52.229958,21.013653
    # print(geocodeapi.get_inv_direction(latitude,longitude))
    # print(get_search_string(latitude,longitude))
    yws = YahooWeatherService(longitude=longitude, latitude=latitude)
    print(yws.get_weather())
    exit(0)
