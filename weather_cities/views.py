import time
import requests
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import ListView
from django.views.generic.base import View
from .models import Weather
from .forms import AddCityForm, DeleteCityForm

from weather.settings_local import API_KEY


def response_api(city_id):
    response = requests.get('https://api.openweathermap.org/data/2.5/weather',
                            params={'id': city_id, 'appid': API_KEY, 'units': 'metric', 'lang': 'ru'})
    return response


class Home(ListView):
    """Home"""

    model = Weather

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AddCityForm
        context['delete_form'] = DeleteCityForm
        return context


class AddCity(View):
    """Добавление города"""

    def post(self, request):
        form = AddCityForm(request.POST)

        if form.is_valid():
            form = form.save(commit=False)
            response = response_api(form.city_id)
            if response.status_code == 200:

                response = response.json()
                form.icon = 'http://openweathermap.org/img/wn/{}.png'.format(response['weather'][0]['icon'])
                form.name = response['name']
                form.description = response['weather'][0]['description']
                form.temp = response['main']['temp']
                form.pressure = response['main']['pressure']
                form.humidity = response['main']['humidity']
                form.speed = response['wind']['speed']
                form.coord_lon = response['coord']['lon']
                form.coord_lat = response['coord']['lat']
                form.sunrise = time.strftime("%H:%M", time.localtime(response['sys']['sunrise'] + response['timezone']))
                form.sunset = time.strftime("%H:%M", time.localtime(response['sys']['sunset'] + response['timezone']))

                form.save()
                messages.success(request, 'Город успешно добавлен.')
            else:
                messages.error(request, response.json()['message'])
        else:
            print(form)
            messages.error(request, "Невалидная форма")
        return redirect('home_url')


class DeleteCity(View):
    """Удаление города"""

    def post(self, request, city_id):
        form = DeleteCityForm(request.POST)

        if form.is_valid():
            city = Weather.objects.get(city_id=city_id)

            city.delete()
            messages.success(request, 'Город успешно удален.')
        else:
            messages.error(request, "Ошибка удаления")
        return redirect('home_url')
