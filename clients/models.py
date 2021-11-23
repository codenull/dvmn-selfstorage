from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


def validate_agreement(value):
    if not value:
        raise ValidationError(
            'Требуется согласие на обработку персональных данных.'
        )


class Client(AbstractUser):
    username = models.CharField(
        'username',
        max_length=150,
        blank=True,
        null=True,
        unique=True
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=50
    )
    patronymic = models.CharField(
        verbose_name='Отчество',
        max_length=50
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=50
    )
    phonenumber = PhoneNumberField(
        verbose_name='Телефон',
    )
    birthday = models.DateField(
        verbose_name='Дата рождения',
        null=True
    ) # прикрутить валидатор проверки совершеннолетия
    passport = models.CharField(
        'Серия и номер паспорта',
        max_length=10,
        validators=[MinLengthValidator(10)],
        null=True
    )
    agreement = models.BooleanField(
        'Согласие на обработку персональных даных',
        validators=[validate_agreement],
        default=True
    )

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        if self.username:
            return self.username
        return f'{self.first_name} {self.last_name}'
