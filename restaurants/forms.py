# restaurants/forms.py

from django import forms

class RestaurantSearchForm(forms.Form):
    name = forms.CharField(required=False, label='Restaurant Name')
    cuisine_type = forms.CharField(required=False, label='Cuisine Type')
    location = forms.CharField(required=False, label='Location')
    min_rating = forms.DecimalField(required=False, min_value=0, max_value=5, label='Minimum Rating')
    max_distance = forms.DecimalField(required=False, min_value=0, label='Maximum Distance (km)')
