from django.urls import path
from . import views

urlpatterns = [
    path('map/', views.restaurant_map, name='restaurant_map'),
    path('toggle-favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('get-favorites/', views.get_favorites, name='get_favorites'),
    path('<str:restaurant_name>/', views.restaurant_detail, name='restaurant_detail'),
]
