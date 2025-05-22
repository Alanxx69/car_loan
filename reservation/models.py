from django.db import models

from customer.models import Customer


class Vehicle(models.Model):
    STATUS_CHOICES = [
        ("available", "Disponível"),  # Traduzido
        ("loaned", "Emprestado"),  # Traduzido
        ("maintenance", "Em Manutenção"),  # Traduzido
    ]

    model = models.CharField(max_length=100)
    license_plate = models.CharField(max_length=20, unique=True)
    year = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="available")

    def __str__(self):
        return f"{self.model} ({self.license_plate})"


class Location(models.Model):
    reference_point = models.CharField(max_length=100)  # Ex: Shopping Morumbi, Aeroporto, etc.
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)  # SP, RJ, etc.

    def __str__(self):
        return f"{self.reference_point} - {self.city}/{self.state}"


class Reservation(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)

    pickup_location = models.ForeignKey(Location, related_name="pickup_reservations", on_delete=models.CASCADE)
    dropoff_location = models.ForeignKey(Location, related_name="dropoff_reservations", on_delete=models.CASCADE)

    pickup_datetime = models.DateTimeField()
    dropoff_datetime = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer} → {self.vehicle} ({self.pickup_datetime.date()} - {self.dropoff_datetime.date()})"
