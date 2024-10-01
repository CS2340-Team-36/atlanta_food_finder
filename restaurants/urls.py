from django.urls import path
from . import views

urlpatterns = [
    path('map/', views.restaurant_map, name='restaurant_map'),
    path('<str:restaurant_name>/', views.restaurant_detail, name='restaurant_detail'),
]
