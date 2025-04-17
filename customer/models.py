from django.conf import settings
from django.db import models


class Customer(models.Model):
    user_id = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    # Exemplo: Tornando telefone e endereço opcionais
    phone = models.CharField(
        max_length=20, unique=True, blank=True, null=True
    )  # unique=True pode ser problemático com null=True em alguns DBs, considere remover unique ou usar um valor padrão único se necessário.
    date_of_birth = models.DateField(blank=True, null=True)  # Data de nascimento opcional
    address = models.TextField(blank=True)  # Endereço opcional (TextField não precisa de null=True)
    city = models.CharField(max_length=50, blank=True)  # Cidade opcional
    state = models.CharField(max_length=50, blank=True)  # Estado opcional
    zip_code = models.CharField(max_length=10, blank=True)  # CEP opcional
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Cuidado ao acessar first_name/last_name se eles pudessem ser blank=True
        return f"{self.first_name or ''} {self.last_name or ''}".strip() or self.email
