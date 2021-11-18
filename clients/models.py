from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


def validate_agreement(value):
    if not value:
        raise ValidationError(
            'Требуется согласие на обработку персональных данных.'
        )


class Client(AbstractUser):

    first_name = models.CharField(
        verbose_name='Имя',
        max_length=50
    )
    patronymic = models.CharField(
        verbose_name='Отчество',
        max_length=50,
        blank=True,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=50
    )
    phonenumber = PhoneNumberField(
        verbose_name='Телефон',
    )
    birthday = models.DateField(
        verbose_name='Дата рождения'
    ) # прикрутить валидатор проверки совершеннолетия
    passport = models.PositiveIntegerField(
        'Серия и номер паспорта',
        validators=[MinValueValidator(10), MaxValueValidator(10)]
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
        return f'{self.username} {self.first_name} {self.last_name}'
