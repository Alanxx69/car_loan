from django.shortcuts import redirect, render

from .models import Vehicle


def vehicle_create(request):
    if request.method == "POST":
        Vehicle.objects.create(
            model=request.POST.get("model"),
            license_plate=request.POST.get("license_plate"),
            year=request.POST.get("year"),
            status=request.POST.get("status", "available"),
        )
        return redirect("vehicle_list")
    return render(request, "vehicle/vehicle_create.html")


def vehicle_list(request):
    vehicles = Vehicle.objects.all()
    return render(request, "vehicle/vehicle_list.html", {"vehicles": vehicles})
