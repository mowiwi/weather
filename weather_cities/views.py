from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import ListView
from django.views.generic.base import View
from .models import Weather, Ordering
from .forms import AddCityForm, DeleteCityForm, OrderingForm
import csv
from django.http import HttpResponse
from .openweathermap_api import response_api, response_group_api, weather_city, weather_group_city

from datetime import datetime
import time


class Home(ListView):
    """Home"""

    model = Weather
    paginate_by = 20

    def get_ordering(self):
        """Return the field or fields to use for ordering the queryset."""
        if Ordering.objects.first():
            return Ordering.objects.first().sort

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AddCityForm
        context['delete_form'] = DeleteCityForm
        context['ordering_form'] = OrderingForm
        return context

    def post(self, request):
        form = OrderingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Сортировка изменена.')
        return redirect('home_url')


class AddCity(View):
    """Добавление города"""

    def post(self, request):
        form = AddCityForm(request.POST)

        if form.is_valid():
            form = form.save(commit=False)
            response = response_api(form.city_id)
            if response.status_code == 200:
                weather = weather_city(response)

                form.icon = weather['icon']
                form.name = weather['name']
                form.description = weather['description']
                form.temp = weather['temp']
                form.pressure = weather['pressure']
                form.humidity = weather['humidity']
                form.speed = weather['speed']
                form.coord_lon = weather['coord_lon']
                form.coord_lat = weather['coord_lat']
                form.sunrise = weather['sunrise']
                form.sunset = weather['sunset']

                form.save()
                messages.success(request, 'Город успешно добавлен.')
            else:
                messages.error(request, response.json()['message'])
        else:
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


def export(request):
    """Экспорт даных в csv файл"""

    response = HttpResponse(content_type='text/csv')

    writer = csv.writer(response)

    writer.writerow(fields.verbose_name for fields in Weather._meta.get_fields()[1:])

    for weather in Weather.objects.all().values_list()[1:]:
        writer.writerow(weather)

    response['Content-Disposition'] = 'attachment; filename="weather.csv"'

    return response


def import_csv(request):
    """Импорт даных с csv файла"""

    if request.method == 'POST' and request.FILES['csv_file']:

        base_city_id_list = [i.city_id for i in Weather.objects.iterator()]
        city_id = []
        city_id_list = ''
        counter = 0
        update_city = 0
        all_city = 0

        for field in request.FILES['csv_file']:
            try:
                field_id = int(field.decode().rstrip('\n'))
                all_city += 1
                if field_id not in base_city_id_list:
                    if counter < 20:
                        city_id_list += str(field_id) + ','
                        counter += 1
                    else:
                        city_id.append(city_id_list[:-1])
                        city_id_list = ''
                        city_id_list += str(field_id) + ','
                        counter = 1
                else:
                    update_city += 1

            except ValueError:
                pass

        city_id.append(city_id_list[:-1])

        created_city = 0
        for c_id in city_id:

            response = response_group_api(c_id)

            if response.status_code == 200:

                weather_group = weather_group_city(response)

                for weather in weather_group:

                    obj, created = Weather.objects.get_or_create(
                        city_id=weather['city_id'],
                        defaults={
                                  'icon': weather['icon'],
                                  'name': weather['name'],
                                  'description': weather['description'],
                                  'temp': weather['temp'],
                                  'pressure': weather['pressure'],
                                  'humidity': weather['humidity'],
                                  'speed': weather['speed'],
                                  'coord_lon': weather['coord_lon'],
                                  'coord_lat': weather['coord_lat'],
                                  'sunrise': weather['sunrise'],
                                  'sunset': weather['sunset']
                                  })

                    if created:
                        created_city += 1

        if created_city:
            messages.success(request, f'Добавлено новых городов: {created_city}.')
        if update_city:
            messages.success(request, f'Пропущено, потому что информация уже доступна: {update_city}.')
        if all_city - created_city - update_city:
            messages.error(request, f'Ошибок получения даных: {all_city - created_city - update_city}.')

    else:
        messages.error(request, "Ошибка")

    return redirect('home_url')


# start_time = datetime.now()
# print(datetime.now() - start_time)
