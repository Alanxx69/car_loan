from django.contrib import messages  # Opcional: para feedback ao usuário
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction  # Importe transaction
from django.shortcuts import redirect, render

from customer.forms import CustomUserCreationForm  # Importa o formulário customizado
from customer.models import Customer  # Importe o modelo Customer


def home(request):
    """View para a página inicial do sistema de empréstimo de veículos."""
    return render(request, "home/home.html")


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
