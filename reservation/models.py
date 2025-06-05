from django.db import models
from django.db.models import Avg
from django.utils import timezone

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


def average_rating(self):
    ratings = VehicleRating.objects.filter(reservation__vehicle=self)
    if ratings.exists():
        return ratings.aggregate(Avg("rating"))["rating__avg"]
    return None


class Location(models.Model):
    reference_point = models.CharField(max_length=100)  # Ex: Shopping Morumbi, Aeroporto, etc.
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)  # SP, RJ, etc.

    def __str__(self):
        return f"{self.reference_point} - {self.city}/{self.state}"


class Reservation(models.Model):
    STATUS_CHOICES = [
        ("active", "Ativa"),
        ("completed", "Concluída"),
        ("canceled", "Cancelada"),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    pickup_location = models.ForeignKey(Location, related_name="pickup_reservations", on_delete=models.CASCADE)
    dropoff_location = models.ForeignKey(Location, related_name="dropoff_reservations", on_delete=models.CASCADE)
    pickup_datetime = models.DateTimeField()
    dropoff_datetime = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="active")

    def __str__(self):
        return f"{self.customer} → {self.vehicle} ({self.pickup_datetime.date()} - {self.dropoff_datetime.date()})"


class VehicleRating(models.Model):
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE, related_name="rating")
    rating = models.IntegerField(
        choices=[(1, "1 Estrela"), (2, "2 Estrelas"), (3, "3 Estrelas"), (4, "4 Estrelas"), (5, "5 Estrelas")]
    )
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Avaliação {self.rating}/5 para {self.reservation.vehicle.model}"


# Adicione o método à classe Vehicle
Vehicle.average_rating = average_rating
