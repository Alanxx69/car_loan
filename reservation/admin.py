from django.contrib import admin

from .models import Location, Reservation, Vehicle

# Register your models here.
admin.site.register(Reservation)
admin.site.register(Location)
admin.site.register(Vehicle)
