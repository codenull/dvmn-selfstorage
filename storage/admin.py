from django.contrib import admin

from .models import Storage, Order, Inventory, Town


admin.site.register([Inventory, Order, Storage, Town])
