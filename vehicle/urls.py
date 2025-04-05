from django.urls import path

from . import views

urlpatterns = [
    path("create/", views.create_vehicle, name="create_vehicle"),
    path("list/", views.vehicle_list, name="vehicle_list"),
]
