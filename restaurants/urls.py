from django.urls import path
from . import views
from .views import toggle_favorite, get_favorites

urlpatterns = [
    path('map/', views.restaurant_map, name='restaurant_map'),
    path('<str:restaurant_name>/', views.restaurant_detail, name='restaurant_detail'),
    path('toggle-favorite/', toggle_favorite, name='toggle_favorite'),
    path('get-favorites/', get_favorites, name='get_favorites'),
]
