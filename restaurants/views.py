import requests
from django.shortcuts import render
from django.conf import settings
from .models import Restaurant
from django.http import JsonResponse
from .models import Restaurant, Favorite
from django.contrib.auth.decorators import login_required
import json

@login_required
def restaurant_map(request):
    restaurants = Restaurant.objects.all()
    context = {"restaurants": restaurants}
    return render(request, "restaurants/map.html", context)

@login_required
def restaurant_detail(request, restaurant_name):
    formatted_name = restaurant_name.replace("-", " ").title()

    api_key = settings.GOOGLE_MAPS_API_KEY_SERVER

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

        place_details_url = "https://maps.googleapis.com/maps/api/place/details/json"
        details_params = {
            "place_id": place_id,
            "fields": "name,rating,formatted_address,reviews,opening_hours,price_level,geometry,types,editorial_summary,formatted_phone_number,website",  # Add contact fields
            "key": api_key,
        }

        details_response = requests.get(place_details_url, params=details_params)
        details_data = details_response.json()

        if details_data.get("result"):
            details = details_data["result"]

            latitude = details.get("geometry", {}).get("location", {}).get("lat")
            longitude = details.get("geometry", {}).get("location", {}).get("lng")

            print("Latitude:", latitude)
            print("Longitude:", longitude)

            types = details.get("types", [])
            name = details.get("name", "")
            website = details.get("website", "")
            editorial_summary = details.get("editorial_summary", {}).get("overview", "")
            reviews = details.get("reviews", [])

            # Function to determine cuisine
            def get_cuisine(types, name, website, editorial_summary, reviews):
                # List of known cuisines
                cuisines = {
                    "Chinese": ["chinese", "dim sum", "dumplings"],
                    "Italian": ["italian", "pasta", "pizza", "risotto"],
                    "Mexican": [
                        "mexican",
                        "tacos",
                        "burritos",
                        "enchiladas",
                        "quesadillas",
                        "taqueria",
                    ],
                    "Indian": ["indian", "curry", "naan", "tandoori"],
                    "Japanese": ["japanese", "sushi", "ramen", "tempura"],
                    "Thai": ["thai", "pad thai", "tom yum", "green curry"],
                    "French": ["french", "baguette", "croissant", "brie"],
                    "American": ["american", "burger", "fries", "steak"],
                    "Mediterranean": ["mediterranean", "hummus", "falafel", "pita"],
                    "Korean": ["korean", "kimchi", "bibimbap", "bulgogi"],
                    "Vietnamese": ["vietnamese", "pho", "banh mi", "spring rolls"],
                    "Spanish": ["spanish", "paella", "tapas", "churros"],
                    "Greek": ["greek", "gyros", "souvlaki", "tzatziki"],
                    "Middle Eastern": [
                        "middle eastern",
                        "shawarma",
                        "hummus",
                        "falafel",
                    ],
                    "Lebanese": ["lebanese", "tabbouleh", "hummus", "shawarma"],
                    "Turkish": ["turkish", "kebab", "baklava", "pide"],
                    "Brazilian": ["brazilian", "feijoada", "churrasco", "brigadeiro"],
                    "Caribbean": ["caribbean", "jerk chicken", "plantains"],
                    "Ethiopian": ["ethiopian", "injera", "doro wat", "berbere"],
                    "German": ["german", "bratwurst", "sauerkraut", "pretzel"],
                    "Irish": ["irish", "shepherd's pie", "corned beef", "guinness"],
                    "Russian": ["russian", "borscht", "pelmeni", "blini"],
                    "Polish": ["polish", "pierogi", "kielbasa"],
                    "African": ["african", "jollof", "fufu", "injera"],
                    "Australian": ["australian", "vegemite", "meat pie"],
                    "Belgian": ["belgian", "waffles", "chocolate"],
                    "Cuban": ["cuban", "ropa vieja", "cubano sandwich"],
                    "Filipino": ["filipino", "adobo", "pancit", "lechon"],
                    "Hawaiian": ["hawaiian", "poke", "spam musubi"],
                    "Hungarian": ["hungarian", "goulash", "langos"],
                    "Indonesian": ["indonesian", "satay", "nasi goreng"],
                    "Malaysian": ["malaysian", "laksa", "satay"],
                    "Pakistani": ["pakistani", "biryani", "nihari"],
                    "Peruvian": ["peruvian", "ceviche", "lomo saltado"],
                    "Portuguese": ["portuguese", "bacalhau", "pastel de nata"],
                    "Scottish": ["scottish", "haggis", "scotch pie"],
                    "South African": ["south african", "biltong", "bobotie"],
                    "Swedish": ["swedish", "meatballs", "gravlax"],
                    "Taiwanese": ["taiwanese", "beef noodle soup", "bubble tea"],
                    "Tex-Mex": ["tex-mex", "nachos", "fajitas"],
                    "Seafood": ["seafood", "lobster", "crab", "shrimp"],
                    "Steakhouse": ["steakhouse", "steak", "ribeye", "sirloin"],
                    "BBQ": ["bbq", "ribs", "brisket", "pulled pork"],
                    "Cafe": ["cafe", "coffee", "espresso", "latte"],
                    "Bakery": ["bakery", "bread", "croissant", "bagel"],
                    "Deli": ["deli", "sandwich", "bagel", "pastrami"],
                    "Bistro": ["bistro", "crepe", "quiche"],
                    "Pub": ["pub", "ale", "fish and chips"],
                    "Grill": ["grill", "barbecue"],
                    "Fusion": ["fusion", "mix", "blend"],
                }

                # Step 1: Check for specific types in the Google Places API 'types' field
                for t in types:
                    if t.endswith("_restaurant"):
                        cuisine_type = (
                            t.replace("_restaurant", "").replace("_", " ").title()
                        )
                        return cuisine_type

                # Step 2: Prioritize checking the restaurant name
                name_lower = name.lower()
                for cuisine, keywords in cuisines.items():
                    if any(keyword in name_lower for keyword in keywords):
                        return cuisine

                # Step 3: Check the editorial summary for keywords
                if editorial_summary:
                    summary_lower = editorial_summary.lower()
                    for cuisine, keywords in cuisines.items():
                        if any(keyword in summary_lower for keyword in keywords):
                            return cuisine

                # Step 4: Check all reviews for cuisine mentions
                for review in reviews:
                    review_text = review.get("text", "").lower()
                    for cuisine, keywords in cuisines.items():
                        if any(keyword in review_text for keyword in keywords):
                            return cuisine

                # Step 5: Check the website URL for cuisine keywords
                if website:
                    website_lower = website.lower()
                    for cuisine, keywords in cuisines.items():
                        if any(keyword in website_lower for keyword in keywords):
                            return cuisine

                # Default to 'Unknown' if no match is found
                return "Unknown"

            # Get cuisine
            cuisine = get_cuisine(types, name, website, editorial_summary, reviews)

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
                    "cuisine": cuisine,
                    "phone_number": details.get("formatted_phone_number", "N/A"),  # Add phone number
                    "website": details.get("website", ""),  # Add website
                    "place_id": place_id,  # Pass the place_id to the template
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
                    "cuisine": "N/A",
                    "phone_number": "N/A",  # Default phone number
                    "website": "",  # Default website
                    "place_id": None,
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
                "cuisine": "N/A",
                "phone_number": "N/A",  # Default phone number
                "website": "",  # Default website
                "place_id": None,
            },
            "GOOGLE_MAPS_API_KEY_CLIENT": settings.GOOGLE_MAPS_API_KEY_CLIENT,
        }

    return render(request, "restaurants/restaurant_detail.html", context)


def ajax_login_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            return function(request, *args, **kwargs)
        else:
            return JsonResponse({'error': 'You must be logged in to perform this action.'}, status=401)
    return wrap

@ajax_login_required
def toggle_favorite(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        restaurant_name = data.get('restaurant_name')
        place_id = data.get('place_id')

        user = request.user

        favorite, created = Favorite.objects.get_or_create(
            user=user,
            restaurant_place_id=place_id,
            defaults={'restaurant_name': restaurant_name}
        )

        if not created:
            # Favorite already exists, so remove it
            favorite.delete()
            favorited = False
        else:
            # Favorite was created
            favorited = True

        # Return the updated list of favorites
        favorites = Favorite.objects.filter(user=user)
        favorites_list = [{
            'restaurant_name': fav.restaurant_name,
            'restaurant_place_id': fav.restaurant_place_id
        } for fav in favorites]

        return JsonResponse({'favorited': favorited, 'favorites': favorites_list})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

@ajax_login_required
def get_favorites(request):
    if request.method == 'GET':
        user = request.user
        favorites = Favorite.objects.filter(user=user)
        favorites_list = [{
            'restaurant_name': fav.restaurant_name,
            'restaurant_place_id': fav.restaurant_place_id
        } for fav in favorites]

        return JsonResponse({'favorites': favorites_list})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)