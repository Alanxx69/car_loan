from django.urls import path

from . import views

urlpatterns = [
    path("profile/update/", views.profile_update, name="profile_update"),
    path("update/<int:pk>/", views.customer_update, name="customer_update"),
    path("list/", views.customer_list, name="customer_list"),
]
