from django.contrib import admin

from .models import Storage, Order, Inventory, Town, InventoryPriceList


admin.site.register([Inventory, InventoryPriceList, Order, Storage, Town])
