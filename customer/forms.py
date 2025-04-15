from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Customer


class CustomUserCreationForm(UserCreationForm):
    # Campos adicionais
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(required=False)
    phone = forms.CharField(max_length=20, required=False)
    date_of_birth = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}))
    address = forms.CharField(max_length=100, required=False)
    city = forms.CharField(max_length=50, required=False)
    state = forms.CharField(max_length=50, required=False)
    zip_code = forms.CharField(max_length=10, required=False)

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "first_name", "last_name", "email")


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        # Liste os campos do modelo Customer que você quer permitir
        # que o usuário edite no formulário.
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
            "date_of_birth",
            "address",
            "city",
            "state",
            "zip_code",
        ]
        # Opcional: Adicionar widgets para customizar a aparência dos campos
        widgets = {
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),  # Usa input de data HTML5
            "address": forms.Textarea(attrs={"rows": 3}),  # Textarea menor
        }
        # Opcional: Definir labels em português se os nomes dos campos no modelo estiverem em inglês
        labels = {
            "first_name": "Primeiro Nome",
            "last_name": "Sobrenome",
            "email": "Email",
            "phone": "Telefone",
            "date_of_birth": "Data de Nascimento",
            "address": "Endereço",
            "city": "Cidade",
            "state": "Estado",
            "zip_code": "CEP",
        }
