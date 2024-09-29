import json
import requests
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from .models import Restaurant


def restaurant_map(request):
    restaurants = Restaurant.objects.all()
    context = {"restaurants": restaurants}
    return render(request, "restaurants/map.html", context)


def restaurant_detail(request, restaurant_name):
    # Replace dashes with spaces and capitalize each word
    formatted_name = restaurant_name.replace("-", " ").title()

    # Use the server-side API key from settings
    api_key = settings.GOOGLE_MAPS_API_KEY_SERVER

    # Search for the place using Place Search API
    place_search_url = (
        "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
    )
    search_params = {
        "input": formatted_name,
        "inputtype": "textquery",
        "fields": "place_id",
        "key": api_key,
    }

    search_response = requests.get(place_search_url, params=search_params)
    search_data = search_response.json()

    if search_data.get("candidates"):
        place_id = search_data["candidates"][0]["place_id"]

        # Get place details using Place Details API
        place_details_url = "https://maps.googleapis.com/maps/api/place/details/json"
        details_params = {
            "place_id": place_id,
            "fields": "name,rating,formatted_address,reviews,opening_hours,price_level,geometry",
            "key": api_key,
        }

        details_response = requests.get(place_details_url, params=details_params)
        details_data = details_response.json()

        if details_data.get("result"):
            details = details_data["result"]

            # Extract latitude and longitude
            latitude = details.get("geometry", {}).get("location", {}).get("lat")
            longitude = details.get("geometry", {}).get("location", {}).get("lng")

            # Debugging: Print latitude and longitude
            print("Latitude:", latitude)
            print("Longitude:", longitude)

            context = {
                "restaurant_name": details.get("name", formatted_name),
                "details": {
                    "description": details.get(
                        "formatted_address", "Address not available."
                    ),
                    "rating": details.get("rating", "N/A"),
                    "price_level": "$" * details.get("price_level", 1),
                    "opening_hours": details.get("opening_hours", {}).get(
                        "weekday_text", []
                    ),
                    "reviews": details.get("reviews", []),
                    "latitude": latitude,
                    "longitude": longitude,
                },
                "GOOGLE_MAPS_API_KEY_CLIENT": settings.GOOGLE_MAPS_API_KEY_CLIENT,
            }
        else:
            context = {
                "restaurant_name": formatted_name,
                "details": {
                    "description": "Details are not available.",
                    "rating": "N/A",
                    "price_level": "N/A",
                    "opening_hours": [],
                    "reviews": [],
                    "latitude": None,
                    "longitude": None,
                },
                "GOOGLE_MAPS_API_KEY_CLIENT": settings.GOOGLE_MAPS_API_KEY_CLIENT,
            }
    else:
        context = {
            "restaurant_name": formatted_name,
            "details": {
                "description": "Details are not available.",
                "rating": "N/A",
                "price_level": "N/A",
                "opening_hours": [],
                "reviews": [],
                "latitude": None,
                "longitude": None,
            },
            "GOOGLE_MAPS_API_KEY_CLIENT": settings.GOOGLE_MAPS_API_KEY_CLIENT,
        }

    return render(request, "restaurants/restaurant_detail.html", context)
