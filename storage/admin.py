from django.contrib import admin

from .models import Storage, Order, Inventory


admin.site.register([Inventory, Order, Storage])
