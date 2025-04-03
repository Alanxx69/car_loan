from django.shortcuts import redirect, render

from .models import Customer


def create_customer(request):
    if request.method == "POST":
        Customer.objects.create(
            first_name=request.POST.get("first_name"),
            last_name=request.POST.get("last_name"),
            email=request.POST.get("email"),
            phone=request.POST.get("phone"),
            date_of_birth=request.POST.get("date_of_birth"),
            address=request.POST.get("address"),
            city=request.POST.get("city"),
            state=request.POST.get("state"),
            zip_code=request.POST.get("zip_code"),
        )
        return redirect("customer_list")
    return render(request, "customer/create_customer.html")


def customer_list(request):
    customers = Customer.objects.all()
    return render(request, "customer/customer_list.html", {"customers": customers})


# Create your views here.
