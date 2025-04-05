from django.shortcuts import redirect, render

from .models import Vehicle


def create_vehicle(request):
    if request.method == "POST":
        Vehicle.objects.create(
            model=request.POST.get("model"),
            license_plate=request.POST.get("license_plate"),
            year=request.POST.get("year"),
            status=request.POST.get("status", "available"),
        )
        return redirect("vehicle_list")
    return render(request, "vehicle/create_vehicle.html")


def vehicle_list(request):
    vehicles = Vehicle.objects.all()
    return render(request, "vehicle/vehicle_list.html", {"vehicles": vehicles})
