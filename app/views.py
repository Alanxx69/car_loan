from django.contrib import messages  # Opcional: para feedback ao usuário
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction  # Importe transaction
from django.shortcuts import redirect, render

from customer.forms import CustomUserCreationForm  # Importa o formulário customizado
from customer.models import Customer  # Importe o modelo Customer
from reservation.models import Location, Vehicle


def home_view(request):
    """
    View para a página inicial
    """
    # Busca as localizações existentes
    locations = Location.objects.all()

    # Gera o range de horas (0-23) para os selects de horário
    hours_range = range(24)

    # Veículos disponíveis para exibição
    available_vehicles = Vehicle.objects.filter(status="available")

    context = {
        "locations": locations,
        "hours_range": hours_range,
        "available_vehicles": available_vehicles,
    }

    return render(request, "home/home.html", context)


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = form.save()

                    customer = Customer.objects.create(
                        user_id=user,
                        first_name=form.cleaned_data.get("first_name"),
                        last_name=form.cleaned_data.get("last_name"),
                        email=form.cleaned_data.get("email"),
                        phone=form.cleaned_data.get("phone"),
                        date_of_birth=form.cleaned_data.get("date_of_birth"),
                        address=form.cleaned_data.get("address"),
                        city=form.cleaned_data.get("city"),
                        state=form.cleaned_data.get("state"),
                        zip_code=form.cleaned_data.get("zip_code"),
                    )

                    messages.success(request, "Registro realizado com sucesso! Faça o login.")
                    return redirect("login")
            except Exception as e:
                messages.error(request, f"Ocorreu um erro durante o registro: {e}")
    else:
        form = CustomUserCreationForm()

    return render(request, "register.html", {"form": form})
