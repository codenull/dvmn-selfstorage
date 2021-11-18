from django.contrib.auth import get_user_model
from django.db import models


Client = get_user_model()


class Storage(models.Model):
    address = models.CharField(max_length=150)
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

    class Meta:
        verbose_name = 'склад'
        verbose_name_plural = 'склады'


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


class InventoryPriceList(models.Model):
    storage = models.ForeignKey(to=Storage,
                                on_delete=models.CASCADE,
                                verbose_name='склад')
    inventory = models.ForeignKey(to=Inventory,
                                  on_delete=models.CASCADE,
                                  verbose_name='инвентарь')
    price_per_week = models.PositiveIntegerField(verbose_name='цена за неделю')
    price_per_month = models.PositiveIntegerField(verbose_name='цена за месяц')


class Order(models.Model):
    client = models.ForeignKey(to=Client,
                               on_delete=models.CASCADE,
                               related_name='box_rental_orders',
                               verbose_name='клиент')
    storage = models.ForeignKey(to='Storage',
                                on_delete=models.SET_NULL,
                                null=True,
                                related_name='clients',
                                verbose_name='склад')
    box_size = models.IntegerField(verbose_name='размер бокса',
                                   null=True,
                                   blank=True)
    inventory = models.ManyToManyField(to='Inventory',
                                       verbose_name='вещи для хранения')
    price = models.PositiveIntegerField(verbose_name='цена хранения')
    start_date = models.DateField(verbose_name='дата начала услуг')
    end_date = models.DateField(verbose_name='дата окончания услуг')

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'
