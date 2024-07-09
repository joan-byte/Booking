from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('reservar/', views.reservar, name='reservar'),
    path('mis_reservas/', views.reservation_list, name='reservation_list'),
    path('registro/', views.registro, name='registro'),
]