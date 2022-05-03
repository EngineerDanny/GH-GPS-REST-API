from django.urls import path
from . import views

urlpatterns = [
      path('get-address/', views.get_address, name='get-address'),
]
