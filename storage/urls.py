from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from . import views


urlpatterns = [path('', views.show_index, name='index'),
               path('season', views.show_season, name='season'),
               path('checkout', views.show_checkout, name='checkout')

               ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
