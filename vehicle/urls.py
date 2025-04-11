from django.urls import path

from . import views

urlpatterns = [
    path("create/", views.vehicle_create, name="vehicle_create"),
    path("list/", views.vehicle_list, name="vehicle_list"),
]
