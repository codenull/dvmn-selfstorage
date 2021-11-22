import datetime
import json
from django.shortcuts import render
from django.http import HttpRequest

from django.http.response import HttpResponseNotFound, JsonResponse
from django.shortcuts import get_object_or_404, render
import monthdelta

from .forms import InventoryOrderForm
from .models import InventoryPriceList, Town
from .models import Storage
from .forms import CalcStorageForm, OrderForm



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


def show_season(request):
    return render(request, 'season.htlml')


def show_checkout(request: HttpRequest):
    storage = None
    if request.method == 'POST':
        return HttpResponseNotFound('<h1>Page not found</h1>')

    context = {
        'price': 100,
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


def inventory_calc(request):
    form = InventoryOrderForm()
    return render(
        request,
        template_name='inventory_calc.html',
        context={'form': form}
    )


def calc_total_price(request, start, end):
    start = datetime.datetime.strptime(start, '%Y-%m-%d')
    end = datetime.datetime.strptime(end, '%Y-%m-%d')
    delta = monthdelta.monthmod(start, end)
    months = delta[0].months
    weeks = round(delta[1].days / 7)
    return JsonResponse({"months":months,"weeks":weeks})


def get_inventory_price(request, storage_id, inventory_id):
    inventory_prices = get_object_or_404(
        InventoryPriceList, storage= storage_id, inventory=inventory_id
    )
    return JsonResponse(
        {'weekPrice': inventory_prices.price_per_week,
         'monthPrice': inventory_prices.price_per_month}
    )
