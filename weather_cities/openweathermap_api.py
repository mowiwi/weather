import time
import requests

from weather.settings_local import API_KEY


def response_api(city_id):
    """API запрос погоды"""

    response = requests.get('https://api.openweathermap.org/data/2.5/weather',
                            params={'id': city_id, 'appid': API_KEY, 'units': 'metric', 'lang': 'ru'})
    return response


def response_group_api(city_id):
    """API запрос погоды"""

    response = requests.get('https://api.openweathermap.org/data/2.5/group',
                            params={'id': city_id, 'appid': API_KEY, 'units': 'metric', 'lang': 'ru'})
    return response


def weather_city(response):
    """Погода в городе"""

    response_json = response.json()
    weather = dict(city_id=response_json['id'],
                   icon='http://openweathermap.org/img/wn/{}.png'.format(response_json['weather'][0]['icon']),
                   name=response_json['name'],
                   description=response_json['weather'][0]['description'],
                   temp=response_json['main']['temp'],
                   pressure=response_json['main']['pressure'],
                   humidity=response_json['main']['humidity'],
                   speed=response_json['wind']['speed'],
                   coord_lon=response_json['coord']['lon'],
                   coord_lat=response_json['coord']['lat'],
                   sunrise=time.strftime("%H:%M", time.localtime(response_json['sys']['sunrise'] + response_json['timezone'])),
                   sunset=time.strftime("%H:%M", time.localtime(response_json['sys']['sunset'] + response_json['timezone']))
                   )
    return weather


def weather_group_city(response):
    """Погода в городе"""

    weather_group = []

    response_group_json = response.json()

    for response_json in response_group_json['list']:
        weather_group.append(
            dict(city_id=response_json['id'],
                 icon='http://openweathermap.org/img/wn/{}.png'.format(response_json['weather'][0]['icon']),
                 name=response_json['name'],
                 description=response_json['weather'][0]['description'],
                 temp=response_json['main']['temp'],
                 pressure=response_json['main']['pressure'],
                 humidity=response_json['main']['humidity'],
                 speed=response_json['wind']['speed'],
                 coord_lon=response_json['coord']['lon'],
                 coord_lat=response_json['coord']['lat'],
                 sunrise=time.strftime("%H:%M",
                                       time.localtime(response_json['sys']['sunrise'] + response_json['sys']['timezone'])),
                 sunset=time.strftime("%H:%M", time.localtime(response_json['sys']['sunset'] + response_json['sys']['timezone']))
                 )
        )
    return weather_group
