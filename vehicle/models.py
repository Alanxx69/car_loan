from django.db import models


# Create your models here.
class Vehicle(models.Model):
    model = models.CharField(max_length=100)
    license_plate = models.CharField(max_length=20, unique=True)
    year = models.IntegerField()
    status = models.CharField(
        max_length=20,
        choices=[("available", "available"), ("loaned", "loaned"), ("maintenance", "maintenance")],
        default="available",
    )
