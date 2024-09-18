from django.db import models

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    cuisine_type = models.CharField(max_length=100, blank=True, null=True)
    opening_hours = models.CharField(max_length=255, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    price_range = models.CharField(max_length=50, blank=True, null=True)
    google_place_id = models.CharField(max_length=255, blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    reviews = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
