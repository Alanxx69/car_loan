from django.contrib import messages  # Para feedback (opcional)
from django.contrib.auth.decorators import login_required  # Importe o decorator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CustomerForm  # <<< ADICIONE ESTA LINHA
from .models import Customer


@login_required
def profile_update(request):
    customer = get_object_or_404(Customer, user_id=request.user)

    if request.method == "POST":
        form = CustomerForm(request.POST, instance=customer)  # <<< USA CustomerForm
        if form.is_valid():
            form.save()
            messages.success(request, "Seu perfil foi atualizado com sucesso!")
            return redirect("profile_update")
        else:
            messages.error(request, "Por favor, corrija os erros abaixo.")
    else:
        form = CustomerForm(instance=customer)  # <<< USA CustomerForm

    return render(request, "customer/customer_update.html", {"form": form})


def customer_update(request, pk):
    customer = get_object_or_404(Customer, pk=pk)  # Busca o cliente ou retorna 404

    if request.method == "POST":
        # Passa request.POST e a instância existente para o formulário
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()  # Salva as alterações no cliente existente
            return redirect("customer_list")  # Redireciona para a lista após salvar
    else:
        # Cria o formulário preenchido com os dados do cliente existente
        form = CustomerForm(instance=customer)

    # Renderiza o template passando o formulário
    # Use um template específico para atualização ou reutilize/adapte o de criação
    return render(request, "customer/customer_update.html", {"form": form, "customer": customer})


def customer_list(request):
    customers = Customer.objects.all()
    return render(request, "customer/customer_list.html", {"customers": customers})


# Create your views here.
