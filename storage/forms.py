import datetime
import monthdelta

from django.forms import fields, forms, models, widgets, Select, NumberInput
from .models import Inventory, Storage


def get_min_duration():
    return datetime.date.today() + datetime.timedelta(weeks=1)


def get_max_duration():
    return datetime.date.today() + monthdelta.monthdelta(6) 


class InventoryOrderForm(forms.Form):
    inventory = models.ModelChoiceField(
        queryset=Inventory.objects,
        label='Что будете хранить',
        widget=widgets.RadioSelect()
    )
    quantity = fields.IntegerField(
        label='В каком количестве',
        widget=widgets.TextInput(
                attrs={'min': 1, 'type': "number", 'style': "width: 30px;"}
        )
    )
    storage = models.ModelChoiceField(
        queryset=Storage.objects,
        label='На каком складе',
        widget=widgets.RadioSelect()
    )
    start_service = fields.DateField(
        label='Дата начала хранения',
        widget=widgets.TextInput(
            attrs={'type': 'date', 'min': datetime.date.today,}
        )
    )
    end_service = fields.DateField(
        label='Дата окончания хранения',
        widget=widgets.TextInput(
                attrs={'type': 'date', 'min': get_min_duration,
                       'max': get_max_duration}
        )
    )

from django import forms
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