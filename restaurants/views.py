import json
from .models import Restaurant
import requests
from django.shortcuts import render, HttpResponse

GOOGLE_PLACES_API_KEY = 'AIzaSyDe39jHRou9FyAwtXDmqtMG2WglTXs7IkA'

def restaurant_map(request):
    restaurants = Restaurant.objects.all()
    context = {'restaurants': restaurants}
    return render(request, 'restaurants/map.html', context)

def restaurant_detail(request, restaurant_name):
    formatted_name = restaurant_name.replace('-', ' ').title()
    place_search_url = f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
    search_params = {
        'input': formatted_name,
        'inputtype': 'textquery',
        'fields': 'place_id',
        'key': GOOGLE_PLACES_API_KEY
    }

    search_response = requests.get(place_search_url, params=search_params)
    search_data = search_response.json()

    if search_data.get('candidates'):
        place_id = search_data['candidates'][0]['place_id']

        place_details_url = f"https://maps.googleapis.com/maps/api/place/details/json"
        details_params = {
            'place_id': place_id,
            'fields': 'name,rating,formatted_address,reviews,opening_hours,price_level',
            'key': GOOGLE_PLACES_API_KEY
        }

        details_response = requests.get(place_details_url, params=details_params)
        details_data = details_response.json()

        if details_data.get('result'):
            details = details_data['result']
            context = {
                'restaurant_name': details.get('name', formatted_name),
                'details': {
                    'description': details.get('formatted_address', 'Address not available.'),
                    'rating': details.get('rating', 'N/A'),
                    'price_level': '$' * details.get('price_level', 1),
                    'opening_hours': details.get('opening_hours', {}).get('weekday_text', []),
                    'reviews': details.get('reviews', [])
                }
            }
        else:
            context = {
                'restaurant_name': formatted_name,
                'details': {
                    'description': 'Details are not available.',
                    'rating': 'N/A',
                    'price_level': 'N/A',
                    'opening_hours': [],
                    'reviews': []
                }
            }
    else:
        context = {
            'restaurant_name': formatted_name,
            'details': {
                'description': 'Details are not available.',
                'rating': 'N/A',
                'price_level': 'N/A',
                'opening_hours': [],
                'reviews': []
            }
        }

    return render(request, 'restaurants/restaurant_detail.html', context)
