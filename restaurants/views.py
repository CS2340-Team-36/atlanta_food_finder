# restaurants/views.py

from django.shortcuts import render
from .models import Restaurant
from .forms import RestaurantSearchForm
from django.core import serializers

def restaurant_search(request):
    form = RestaurantSearchForm(request.GET or None)
    restaurants = Restaurant.objects.all()

    if form.is_valid():
        name = form.cleaned_data.get('name')
        cuisine_type = form.cleaned_data.get('cuisine_type')
        location = form.cleaned_data.get('location')
        min_rating = form.cleaned_data.get('min_rating')
        max_distance = form.cleaned_data.get('max_distance')

        if name:
            restaurants = restaurants.filter(name__icontains=name)
        if cuisine_type:
            restaurants = restaurants.filter(cuisine_type__icontains=cuisine_type)
        if location:
            restaurants = restaurants.filter(location__icontains=location)
        if min_rating:
            restaurants = restaurants.filter(rating__gte=min_rating)
        if max_distance:
            restaurants = restaurants.filter(distance__lte=max_distance)
    restaurant_data = serializers.serialize('json', restaurants)
    return render(request, 'restaurants/index.html', {
        'form': form,
        'restaurants': restaurants,
        'restaurant_data': restaurant_data
    })