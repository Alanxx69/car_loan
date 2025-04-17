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
        widgets = {
            "date_of_birth": forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
            # ... outros widgets ...
        }
        labels = {  # <<< ADICIONE ESTE DICIONÁRIO
            "first_name": "Nome",
            "last_name": "Sobrenome",
            "email": "E-mail",
            "phone": "Telefone",
            "date_of_birth": "Data de Nascimento",
            "address": "Endereço",
            "city": "Cidade",
            "state": "Estado",
            "zip_code": "CEP",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({"class": "form-control"})
            if field_name == "date_of_birth":
                # Remove a classe form-control padrão se quiser usar apenas 'type=date'
                # ou ajuste conforme necessário
                pass
