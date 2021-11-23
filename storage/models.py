from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models


Client = get_user_model()


class Town(models.Model):
    name = models.CharField(max_length=150, verbose_name='название города')
    longitude = models.FloatField(verbose_name='долгота',
                                  blank=True,
                                  null=True)
    latitude = models.FloatField(verbose_name='широта',
                                 null=True,
                                 blank=True)

    class Meta:
        verbose_name = 'город'
        verbose_name_plural = 'города'

    def __str__(self):
        return self.name


class Storage(models.Model):
    town = models.ForeignKey(to='Town',
                             on_delete=models.SET_NULL,
                             null=True,
                             verbose_name='город')
    address = models.CharField(max_length=150, verbose_name='адрес')
    longitude = models.FloatField(verbose_name='долгота',
                                  blank=True,
                                  null=True)
    latitude = models.FloatField(verbose_name='широта',
                                 null=True,
                                 blank=True)
    description = models.TextField(blank=True,
                                   verbose_name='короткое описание')
    picture = models.ImageField(
        upload_to='storage/',
        verbose_name='изображение'
    )
    first_square_meter_price = models.PositiveIntegerField(
        verbose_name='цена за первый метр'
    )
    rest_meters_price = models.PositiveIntegerField(
        verbose_name='цена за каждый последующий метр'
    )
    stored_items = models.ManyToManyField(to='Inventory',
                                          through='InventoryPriceList',
                                          verbose_name='хранимые вещи')

    def calc_price(self, size, months):
        if size <= 0 or months <= 0:
            return 0
        return (self.first_square_meter_price + (size - 1) * self.rest_meters_price) * months
    class Meta:
        verbose_name = 'склад'
        verbose_name_plural = 'склады'

    def __str__(self):
        return self.address

    def serialize(self):
        return {
            "id": self.pk,
            "name": f'{self}',
            "address": self.address,
            "description": self.description,
            "first_square_meter_price": self.first_square_meter_price,
            "rest_meters_price": self.rest_meters_price
        }



class Inventory(models.Model):
    name = models.CharField(max_length=100,
                            unique=True,
                            verbose_name='название')
    picture = models.ImageField(
        upload_to='iventory/',
        verbose_name='изображение инвентаря'
    )

    class Meta:
        verbose_name = 'инвентарь для хранения'
        verbose_name_plural = 'хранимые вещи'

    def __str__(self):
        return self.name


class InventoryPriceList(models.Model):
    storage = models.ForeignKey(to=Storage,
                                on_delete=models.CASCADE,
                                verbose_name='склад')
    inventory = models.ForeignKey(to=Inventory,
                                  on_delete=models.CASCADE,
                                  verbose_name='инвентарь')
    price_per_week = models.PositiveIntegerField(verbose_name='цена за неделю')
    price_per_month = models.PositiveIntegerField(verbose_name='цена за месяц')

    class Meta:
        verbose_name = 'инвентарь для хранения - цена'
        verbose_name_plural = 'прайс по инвентарю'

    def __str__(self):
        return f'{self.storage.address} - {self.inventory.name}'


class Order(models.Model):
    class PaymentStatus(models.IntegerChoices):
        IS_NOT_PAID = 0, 'Заказ не оплачен'
        IS_PAID = 1, 'Заказ оплачен'

    client = models.ForeignKey(to=Client,
                               on_delete=models.CASCADE,
                               related_name='orders',
                               verbose_name='клиент')
    storage = models.ForeignKey(to='Storage',
                                on_delete=models.SET_NULL,
                                null=True,
                                related_name='clients',
                                verbose_name='склад')
    box_size = models.IntegerField(verbose_name='размер бокса',
                                   null=True,
                                   blank=True)
    inventory = models.ForeignKey(to='Inventory',
                                  on_delete=models.SET_NULL,
                                  related_name='orders',
                                  null=True,
                                  verbose_name='вещи для хранения')
    quantity = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Количество вещей'
    )
    payment_status = models.PositiveSmallIntegerField(
        choices=PaymentStatus.choices,
        default=PaymentStatus.IS_NOT_PAID,
        verbose_name='Статус оплаты заказа'
    )
    price = models.PositiveIntegerField(verbose_name='цена хранения')
    start_date = models.DateField(verbose_name='дата начала услуг')
    end_date = models.DateField(verbose_name='дата окончания услуг')

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'
