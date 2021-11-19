import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Town
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
        'storages': json.dumps(get_mock_storages())
    }
    return render(request, 'calc.html', context)


def get_mock_storages():
    return [
        {
            "id": 1,
            "name": "Воронеж-Фрахт",
            "address": "Воронеж, ул. Минская д. 16",
            "description": "",
            "picture": "",
            "first_square_meter_price": 599,
            "rest_meters_price": 150
        },
        {
            "id": 2,
            "name": "Каскад-Воронеж",
            "address": "Воронеж, ул. Ленина д. 5",
            "description": "",
            "picture": "",
            "first_square_meter_price": 400,
            "rest_meters_price": 100
        },
        {
            "id": 3,
            "name": "Кладовка ООО",
            "address": "Воронеж, ул. Ворошилова д. 104",
            "description": "",
            "picture": "",
            "first_square_meter_price": 450,
            "rest_meters_price": 120
        }
    ]
