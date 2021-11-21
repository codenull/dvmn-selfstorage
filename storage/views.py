import datetime
import json

from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render
import monthdelta

from .forms import InventoryOrderForm
from .models import InventoryPriceList, Town
from .models import Storage


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


def show_checkout(request):
    return render(request, 'checkout.html')


def show_calc(request):
    context = {
        'storages': json.dumps(get_serialized_storages())
    }
    return render(request, 'calc.html', context)


def get_serialized_storages():
    storages = [storage.serialize() for storage in Storage.objects.all()]
    return storages


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
