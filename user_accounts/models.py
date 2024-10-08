# restaurants/models.py

from django.db import models

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    cuisine_type = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    distance = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name
