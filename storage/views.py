import datetime
import json

from django import urls
from django.shortcuts import redirect, render
from django.http import HttpRequest
from django.http.response import HttpResponseNotFound, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET, require_POST

import monthdelta

from .forms import CustomUserCreationForm, InventoryOrderForm
from .models import Client, InventoryPriceList, Order, Town
from .models import Storage
from .forms import CalcStorageForm, OrderForm


@require_GET
def show_index(request):
    town = Town.objects.get(name="Воронеж")
    locations = {"town": {"location": [town.longitude, town.latitude]},
                 "storages": []}
    storages = Storage.objects.filter(town=town)
    for storage in storages:
        locations["storages"].append(
            {"location": [storage.longitude, storage.latitude],
             "short_description": storage.description,
             "address": storage.address}
        )
    context = {"locations": locations}
    return render(request, 'index.html', context=context)


def show_checkout(request: HttpRequest):
    if request.method != 'POST':
        return HttpResponseNotFound('<h1>Page not found</h1>')

    storage = get_object_or_404(Storage, pk=request.POST.get('storage_id'))

    price = 0
    storage_box = {}
    if request.POST.get('source_page', None) == 'calc':
        storage_box = {
            'storage_id': storage.pk,
            'size': int(request.POST.get('storage_size')),
            'time': int(request.POST.get('storage_time')),
        }
        price = storage.calc_price(storage_box['size'], storage_box['time'])

    context = {
        'price': price,
        'storage_box': storage_box,
        'forms': {
            'order': OrderForm()
        }
    }

    return render(request, 'checkout.html', context)


def show_calc(request):
    context = {
        'storages': json.dumps(get_serialized_storages()),
        'forms': {
            'calc': CalcStorageForm()
        }
    }
    return render(request, 'calc.html', context)


def get_serialized_storages():
    storages = [storage.serialize() for storage in Storage.objects.all()]
    return storages


def show_order(request):
    return render(request, 'order.html')


def create_order(request):
    return JsonResponse({'message': 'Аренда успешно оформлена.'})
#------------------------------------------------------------------
"""
Контроллеры для калькулятора сезонного хранения инвентаря
"""
@require_GET
def inventory_calc(request):
    form = InventoryOrderForm()
    context = {
        'inventory': zip(form['inventory'],
                         form['inventory'].field.queryset),
        'form': form,
    }
    return render(request, 'season.html', context)


def get_inventory_price(request, storage_id, inventory_id):
    inventory_prices = get_object_or_404(
        InventoryPriceList, storage=storage_id, inventory=inventory_id
    )
    return JsonResponse(
        {'weekPrice': inventory_prices.price_per_week,
         'monthPrice': inventory_prices.price_per_month}
    )


def calc_total_price(request, start, end):
    start = datetime.datetime.strptime(start, '%Y-%m-%d')
    end = datetime.datetime.strptime(end, '%Y-%m-%d')
    delta = monthdelta.monthmod(start, end)
    months = delta[0].months
    weeks = round(delta[1].days / 7)
    return JsonResponse({"months": months, "weeks": weeks})

"""
Контроллеры для оформления заказа
"""
@require_POST
def personal_data(request, storage_type):
    client_form = CustomUserCreationForm()
    if storage_type == 'box':
        order_form = ...
    else:
        order_form = InventoryOrderForm(request.POST)
    return render(
        request,
        'personal_data.html',
        {'client_form': client_form,
        'order_form': order_form,}
    )

@require_POST
def payment(request, storage_type):
    client_form = CustomUserCreationForm(request.POST)
    if storage_type == 'box':
        order_form = ...
    else:
        order_form = InventoryOrderForm(request.POST)
    client_form = CustomUserCreationForm(request.POST)
    return render(
        request,
        'payment.html',
        {'client_form': client_form, 'order_form': order_form,}
    )

@require_POST
def save_order(request, storage_type):
    client_form = CustomUserCreationForm(request.POST)
    client_form.is_valid()
    try:
        client = Client.objects.get(**client_form.cleaned_data)
    except Client.DoesNotExist:
        client = Client.objects.create(
            is_active=True,
            is_superuser=False,
            is_staff=False,
            **client_form.cleaned_data
        )
    if storage_type == 'box':
        ...
        return render(request, 'order_success.html', )
    inventory_order_form = InventoryOrderForm(request.POST)
    inventory_order_form.is_valid()
    Order.objects.create(client=client, **inventory_order_form.cleaned_data)
    return render(request,
                  'order_success.html',
                  {'order_form': inventory_order_form}
                )
