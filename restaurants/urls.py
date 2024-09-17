# restaurants/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('restaurants', views.restaurant_search, name='restaurant_search'),
]
