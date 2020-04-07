from weather.celery import app
from .models import Weather
from .openweathermap_api import response_group_api, weather_group_city


@app.task
def update_weather():

    base_city_id_list = [i.city_id for i in Weather.objects.iterator()]
    city_id = []
    city_id_list = ''
    counter = 0

    for field_id in base_city_id_list:

        if counter < 20:
            city_id_list += str(field_id) + ','
            counter += 1
        else:
            city_id.append(city_id_list[:-1])
            city_id_list = ''
            city_id_list += str(field_id) + ','
            counter = 1
    city_id.append(city_id_list[:-1])
    print(city_id)

    for c_id in city_id:

        response = response_group_api(c_id)

        if response.status_code == 200:

            weather_group = weather_group_city(response)

            for weather in weather_group:

                Weather.objects.filter(city_id=weather['city_id']).update(
                    icon=weather['icon'],
                    name=weather['name'],
                    description=weather['description'],
                    temp=weather['temp'],
                    pressure=weather['pressure'],
                    humidity=weather['humidity'],
                    speed=weather['speed'],
                    coord_lon=weather['coord_lon'],
                    coord_lat=weather['coord_lat'],
                    sunrise=weather['sunrise'],
                    sunset=weather['sunset']
                )

