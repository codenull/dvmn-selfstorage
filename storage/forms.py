import datetime
import monthdelta

from phonenumber_field.formfields import PhoneNumberField
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
                attrs={
                    'min': 1,
                    'type': "number",
                    'class': "form-control form-control-md",
                    'style': "width: 60px;"
                }
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
                attrs={'type': 'date',
                       'min': get_min_duration,
                       'max': get_max_duration
                    }
                )
            )

class CalcStorageForm(forms.Form):
    def __init__(self, **kwargs):
        storage_choices = ((storage.pk, str(storage))
                           for storage in Storage.objects.all())
        self.selected_storage = fields.ChoiceField(
            choices=storage_choices,
            label='',
            widget=Select(attrs={
                'class': 'form-select',
                'id': 'selected_storage',
                'value': 0
            })
        )
        self.storage_time = fields.IntegerField(
            min_value=1, max_value=12,
            widget=NumberInput(attrs={
                'type': 'range',
                'min': 1,
                'max': 12,
                'step': 1,
                'value': 3,
                'list': 'timeMarks'
            }))
        self.storage_size = fields.IntegerField(
            min_value=1, max_value=20,
            widget=NumberInput(attrs={
                'type': 'range',
                'min': 1,
                'max': 20,
                'step': 1,
                'value': 3,
                'list': 'sizeMarks'
            }))

        super().__init__(**kwargs)

    class Meta:
        fields = (
            'selected_storage',
            'storage_size',
            'storage_time',
        )


class OrderForm(forms.Form):
    client_first_name = fields.CharField(
        label='Имя', 
        max_length=50, 
        widget=widgets.TextInput(attrs={
            'id': 'InputFirstName',
            'class': 'form-control',
            'aria-describedby': 'nameHelp',
            'placeholder': 'Иван',
            'required': ''
        }))
    
    client_last_name = fields.CharField(
        label='Фамилия', 
        max_length=50, 
        widget=widgets.TextInput(attrs={
            'id': 'InputSecondName',
            'class': 'form-control',
            'aria-describedby': 'surnameHelp',
            'placeholder': 'Иванов',
            'required': ''
        }))
    
    client_patronymic = fields.CharField(
        label='Отчество', 
        max_length=50, 
        widget=widgets.TextInput(attrs={
            'id': 'PatrName',
            'class': 'form-control',
            'aria-describedby': 'patrnameHelp',
            'placeholder': 'Иванович',
            'required': ''
        }))
    
    client_birthday = fields.DateField(
        label='Дата рождения',
        widget=widgets.DateInput(
            attrs={
                'id': 'InputBirthday',
                'type': 'date',
                'class': 'form-control',
            }
        )
    )
    
    client_passport = fields.CharField(
        label='Паспорт', 
        max_length=50, 
        widget=widgets.TextInput(attrs={
            'id': 'InputPasNumber',
            'class': 'form-control',
            'aria-describedby': 'patrnameHelp',
            'placeholder': '4123 456789',
            'required': ''
        }))
    
    client_phonenumber = PhoneNumberField(
        widget=fields.TextInput(attrs={
            'id': 'InputPhone',
            'placeholder': '',
            'class': 'form-control',
            'aria-describedby': 'phoneHelp',
            'placeholder': '+79991234567',
            'required': ''
        }))

    

    card_num = ''
    card_owner = ''
    card_exp = ''
    card_cvv = ''

