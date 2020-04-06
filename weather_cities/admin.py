from django.contrib import admin
from .models import Weather, Ordering


@admin.register(Weather)
class WeatherAdmin(admin.ModelAdmin):
    pass


@admin.register(Ordering)
class OrderingAdmin(admin.ModelAdmin):
    pass
