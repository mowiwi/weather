from django import forms
from .models import Weather


class AddCityForm(forms.ModelForm):
    """Форма добавления города"""

    class Meta:
        model = Weather
        fields = ("city_id",)


class DeleteCityForm(forms.ModelForm):
    """Форма удаления города"""

    class Meta:
        model = Weather
        fields = ()
