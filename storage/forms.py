import datetime

from django.forms import fields, forms, models, widgets
import monthdelta

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
