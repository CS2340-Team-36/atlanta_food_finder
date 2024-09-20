from django.shortcuts import render
from .models import Restaurant

def restaurant_map(request):
    restaurants = Restaurant.objects.all()
    context = {'restaurants': restaurants}
    return render(request, 'restaurants/map.html', context)