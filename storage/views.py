from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import json


def show_index(request):
    return render(request, 'index.html')


def show_season(request):
    return render(request, 'season.htlml')


def show_checkout(request):
    return render(request, 'checkout.html')

def show_calc(request):
    context = {
        'storages': json.dump(get_mock_storages())
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
