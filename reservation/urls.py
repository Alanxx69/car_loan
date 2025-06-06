from django.urls import path

from . import views

urlpatterns = [
    path("create-reservation/", views.create_reservation, name="create_reservation"),
    path("reservation/<int:reservation_id>/", views.reservation_detail, name="reservation_detail"),
    path("search-vehicles/", views.search_vehicles, name="search_vehicles"),
    path("my-reservations/", views.my_reservations, name="my_reservations"),  # NOVA URL
    path("reservation/<int:reservation_id>/rate/", views.rate_vehicle, name="rate_vehicle"),
    path("api/update_status/", views.api_update_reservation_status, name="api_update_reservation_status"),
    path("api/update_status/", views.api_update_reservation_status, name="api_update_reservation_status"),
]
