from django.urls import path
from . import views

urlpatterns = [
      path('get-address', views.get_address, name='get-address'),
      path('get-gps', views.get_gps, name='get_gps'),
]
