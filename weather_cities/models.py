from django.db import models


class Weather(models.Model):
    """Погода"""
    city_id = models.PositiveIntegerField('Id города', unique=True)
    icon = models.URLField('Картинка погоды')
    name = models.CharField('Город', max_length=100)
    description = models.CharField('Погодные условия', max_length=100)
    temp = models.FloatField('Температура')
    pressure = models.PositiveSmallIntegerField('Атмосферное давление')
    humidity = models.PositiveSmallIntegerField('Влажность воздуха')
    speed = models.PositiveSmallIntegerField('Скорость ветра')
    coord_lon = models.FloatField('Географические координаты - долгота')
    coord_lat = models.FloatField('Географические координаты - широта')
    sunrise = models.TimeField('Восход')
    sunset = models.TimeField('Закат')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Погода"
        verbose_name_plural = "Погода"
