# Generated by Django 3.0.5 on 2020-04-07 11:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Weather',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city_id', models.PositiveIntegerField(verbose_name='ID города')),
                ('icon', models.URLField(verbose_name='Картинка погоды')),
                ('name', models.CharField(max_length=100, verbose_name='Город')),
                ('description', models.CharField(max_length=100, verbose_name='Погодные условия')),
                ('temp', models.FloatField(verbose_name='Температура')),
                ('pressure', models.PositiveSmallIntegerField(verbose_name='Атмосферное давление')),
                ('humidity', models.PositiveSmallIntegerField(verbose_name='Влажность воздуха')),
                ('speed', models.PositiveSmallIntegerField(verbose_name='Скорость ветра')),
                ('coord_lon', models.FloatField(verbose_name='Географические координаты - долгота')),
                ('coord_lat', models.FloatField(verbose_name='Географические координаты - широта')),
                ('sunrise', models.TimeField(verbose_name='Восход')),
                ('sunset', models.TimeField(verbose_name='Закат')),
                ('user', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Погода',
                'verbose_name_plural': 'Погода',
            },
        ),
        migrations.CreateModel(
            name='Ordering',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort', models.CharField(choices=[('city_id', 'ID города: по возростанию'), ('-city_id', 'ID города: по убыванию'), ('name', 'Город: по возростанию'), ('-name', 'Город: по убыванию'), ('temp', 'Температура: по возростанию'), ('-temp', 'Температура: по убыванию')], default='city_id', max_length=10, verbose_name='Сортировать по:')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Настройки сортировки',
                'verbose_name_plural': 'Настройки сортировки',
            },
        ),
    ]
