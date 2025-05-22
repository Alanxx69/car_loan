from django.urls import path

from . import views

urlpatterns = [
    path("create-reservation/", views.create_reservation, name="create_reservation"),
    path("reservation/<int:reservation_id>/", views.reservation_detail, name="reservation_detail"),
    path("search-vehicles/", views.search_vehicles, name="search_vehicles"),
]
