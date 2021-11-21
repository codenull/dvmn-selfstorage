from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('', views.show_index, name='index'),
    path('season', views.show_season, name='season'),
    path('checkout', views.show_checkout, name='checkout'),
    path('calc', views.show_calc, name='calc'),
    path('test_season', views.inventory_calc, name='inventory'),
    path('inventory_price/<int:storage_id>/<int:inventory_id>', views.get_inventory_price),
    path('get_price/<str:start>/<str:end>', views.calc_total_price),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
