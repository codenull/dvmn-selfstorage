from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def show_index(request):
    return render(request, 'index.html')


def show_season(request):
    return render(request, 'season.htlml')


def show_checkout(request):
    return render(request, 'checkout.html')

def show_calc(request):
    return render(request, 'calc.html')