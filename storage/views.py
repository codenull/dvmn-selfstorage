import json
from django.shortcuts import render
from django.http import HttpRequest

from .models import Town
from .models import Storage
from .forms import CalcStorageForm



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
        pass


    return render(request, 'checkout.html')


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


