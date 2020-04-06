from django.urls import path
from .views import *

urlpatterns = [
    path('', Home.as_view(), name='home_url'),
    path('add_city/', AddCity.as_view(), name="add_city_url"),
    path('delete_city/<int:city_id>/', DeleteCity.as_view(), name="delete_city_url"),
    path('export/', export, name='export_url'),
    path('import/', import_csv, name='import_csv_url'),
]
