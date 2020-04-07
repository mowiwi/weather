from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Weather(models.Model):
    """Погода"""
    user = models.ManyToManyField(User)
    city_id = models.PositiveIntegerField('ID города')
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


class Ordering(models.Model):
    """Сортировка"""
    CHOICES = (
        ('city_id', 'ID города: по возростанию'),
        ('-city_id', 'ID города: по убыванию'),
        ('name', 'Город: по возростанию'),
        ('-name', 'Город: по убыванию'),
        ('temp', 'Температура: по возростанию'),
        ('-temp', 'Температура: по убыванию'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sort = models.CharField('Сортировать по:', max_length=10,
                            choices=CHOICES,
                            default='city_id')

    class Meta:
        verbose_name = "Настройки сортировки"
        verbose_name_plural = "Настройки сортировки"

    @receiver(post_save, sender=User)
    def create_user_ordering(sender, instance, created, **kwargs):
        if created:
            Ordering.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_ordering(sender, instance, **kwargs):
        instance.ordering.save()

    def __str__(self):
        return f'Настройки сортировки для {self.user}'
