from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views


urlpatterns = [
    path('', views.show_index, name='index'),
    # Mаршруты для калькулятора сезонного хранения
    path('inventory_calc', views.inventory_calc, name='season'),
    # эндпоинт для JS для получения информации о цене на конкретном складе
    path('inventory_calc/price/<int:storage_id>/<int:inventory_id>',
         views.get_inventory_price
    ),
    # эндпоинт для JS для получения итоговой цены
    path('inventory_calc/calc_total_price/<str:start>/<str:end>',
         views.calc_total_price),
    # Маршруты для оформления заказа после работы с калькулятором
    path('order/personal_data/<str:storage_type>',
         views.personal_data,
         name='personal_data'),
    path('order/payment/<str:storage_type>', views.payment, name='payment'),
    path('order/save_order/<str:storage_type>',
         views.save_order,
         name='save_order'),
    #--------------------------------------------------------------
    path('checkout', views.show_checkout, name='checkout'),
    path('calc', views.show_calc, name='calc'),

    path('order', views.show_order, name='order'),
    path('order/create', views.create_order, name='order_create'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
