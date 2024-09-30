import requests
from django.conf import settings
from django.shortcuts import render

# Function to interact with Google Places API for Nearby Search
def search_restaurants_nearby(location, radius=1500, keyword="restaurant"):
    api_key = settings.GOOGLE_API_KEY
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location}&radius={radius}&keyword={keyword}&key={api_key}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json().get('results', [])
    return []

# Function to get detailed information about a specific place using place_id
def get_place_details(place_id):
    api_key = settings.GOOGLE_API_KEY
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={api_key}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json().get('result', {})
    return {}

# View to search for nearby restaurants
def search_restaurants_view(request):
    location = "33.7490,-84.3880"  # Example: Atlanta coordinates
    restaurants = search_restaurants_nearby(location)
    return render(request, 'restaurant_details/restaurant_search.html', {'restaurants': restaurants})

# View to display detailed restaurant info using Google Places API
def restaurant_detail_view(request, place_id):
    restaurant_details = get_place_details(place_id)  
    return render(request, 'restaurant_details/restaurant_detail.html', {'restaurant': restaurant_details})