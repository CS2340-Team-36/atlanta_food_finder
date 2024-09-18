from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search_restaurants_view, name='restaurant_search'),
    path('details/<place_id>/', views.restaurant_detail_view, name='restaurant_detail'),
]
