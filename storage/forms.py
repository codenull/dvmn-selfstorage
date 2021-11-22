from django import forms
from django.db.models import fields
from django.forms import widgets, Select, NumberInput
from .models import Storage


class CalcStorageForm(forms.Form):
    storage_choices = ((storage.pk, str(storage))
                       for storage in Storage.objects.all())
    selected_storage = forms.ChoiceField(
        choices=storage_choices,
        label='',
        widget=Select(attrs={
            'class': 'form-select',
            'id': 'selected_storage',
            'value': 0
        })
    )
    storage_time = forms.IntegerField(
        min_value=1, max_value=12,
        widget=NumberInput(attrs={
            'type': 'range',
            'min': 1,
            'max': 12,
            'step': 1,
            'value': 3,
            'list': 'timeMarks'
        }))
    storage_size = forms.IntegerField(
        min_value=1, max_value=20,
        widget=NumberInput(attrs={
            'type': 'range',
            'min': 1,
            'max': 20,
            'step': 1,
            'value': 3,
            'list': 'sizeMarks'
        }))

    class Meta:
        fields = (
            'selected_storage',
            'storage_size',
            'storage_time',
        )
