from django import forms
from .models import Weather, Ordering


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


class OrderingForm(forms.ModelForm):
    """Форма сортивовки"""

    class Meta:
        model = Ordering
        fields = ('sort',)
