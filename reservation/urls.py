from django.urls import path

from . import views

urlpatterns = [
    path("create-reservation/", views.create_reservation, name="create_reservation"),
    path("search-vehicles/", views.search_vehicles, name="search_vehicles"),
]
