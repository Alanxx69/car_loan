from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render


def home(request):
    """View para a página inicial do sistema de empréstimo de veículos."""
    return render(request, "home.html")


def register(request):
    """View para registro de novos usuários."""
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})
