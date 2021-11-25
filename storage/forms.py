import datetime
import monthdelta

from django.contrib.auth import get_user_model
from django.forms import ModelForm
from django.forms import fields, forms, models, widgets, Select, NumberInput
from phonenumber_field.formfields import PhoneNumberField

from .models import Order, Storage


def get_min_duration():
    return datetime.date.today() + datetime.timedelta(weeks=1)


def get_max_duration():
    return datetime.date.today() + monthdelta.monthdelta(6)


class InventoryOrderForm(models.ModelForm):
    class Meta:
        model = Order
        fields = ('inventory', 'quantity', 'storage',
                  'start_date', 'end_date', 'price')
        widgets = {
            'inventory': widgets.RadioSelect(),
            'storage': widgets.RadioSelect(),
            'quantity': widgets.TextInput(
                attrs={'min': 1, 'type': "number",
                       'class': "form-control form-control-md",
                       'style': "width: 60px;"}
                ),
            'price': widgets.HiddenInput(),
            'start_date': widgets.TextInput(
                attrs={'type': 'date',
                       'min': datetime.date.today,
                    }
                ),
            'end_date': widgets.TextInput(
                attrs={'type': 'date',
                       'min': get_min_duration,
                       'max': get_max_duration
                    }
                )
            }


class CustomUserCreationForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, formfield in self.fields.items():
            if name == 'agreement':
                formfield.widget.attrs["class"] = "form-check-input ms-2"
            else:
                formfield.widget.attrs["class"] = "form-control mb-2"
                if name == 'passport':
                    formfield.widget.attrs["minlength"] = 10
                if name == 'email':
                    formfield.required = True
                if name == 'birthday':
                    formfield.widget = widgets.TextInput(
                        attrs={'type': 'date', 'class':"form-control mb-2"}
                    )
                    formfield.required = True

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'patronymic', 'last_name', 'birthday',
                  'email', 'passport', 'phonenumber', 'agreement',)

# -----------------------------------------

class CalcStorageForm(forms.Form):
    
    storage_time = fields.IntegerField(min_value=1, max_value=12,)
    storage_size = fields.IntegerField(min_value=1, max_value=20)
    selected_storage = fields.ChoiceField()

    def __init__(self,  *args, **kwargs):
        storage_choices = ((storage.pk, str(storage))
                           for storage in Storage.objects.all())
        CalcStorageForm.declared_fields['selected_storage'].choices = storage_choices
        
        super().__init__( *args, **kwargs)

    class Meta:
        fields = ('selected_storage', 'storage_size', 'storage_time')
        widgets = {
            'selected_storage': Select(attrs={
                'class': 'form-select',
                'id': 'selected_storage',
                'value': 0
            }),
            'storage_time': NumberInput(attrs={
                'type': 'range',
                'min': 1,
                'max': 12,
                'step': 1,
                'value': 3,
                'list': 'timeMarks'
            }),
            'storage_size': NumberInput(attrs={
                'type': 'range',
                'min': 1,
                'max': 20,
                'step': 1,
                'value': 3,
                'list': 'sizeMarks'
            }),
        }

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
