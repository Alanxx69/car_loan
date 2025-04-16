from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import models
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .models import Location, Reservation, Vehicle

# Create your views here.


@login_required
def create_reservation(request):
    if request.method == "POST":
        try:
            # Obter ou verificar o cliente (assumindo que o cliente está associado ao usuário)
            user = request.user

            # Obter dados do formulário
            vehicle_id = request.POST.get("vehicle_id")
            pickup_location_str = request.POST.get("pickup_location")
            dropoff_location_str = request.POST.get("dropoff_location")
            pickup_date = request.POST.get("pickup_date")
            pickup_time = request.POST.get("pickup_time")
            dropoff_date = request.POST.get("dropoff_date")
            dropoff_time = request.POST.get("dropoff_time")

            # Validação básica
            if not all([vehicle_id, pickup_location_str, pickup_date, pickup_time, dropoff_date, dropoff_time]):
                messages.error(request, "Todos os campos obrigatórios devem ser preenchidos.")
                return redirect("home")

            # Obter o veículo
            vehicle = get_object_or_404(Vehicle, pk=vehicle_id)

            # Verificar se o veículo está disponível
            if vehicle.status != "available":
                messages.error(request, "Este veículo não está disponível para reserva.")
                return redirect("home")

            # Processar localização (obter existente ou criar nova)
            def get_or_create_location(location_str):
                try:
                    # Tentar encontrar localização existente
                    return Location.objects.get(reference_point=location_str)
                except Location.DoesNotExist:
                    # Criar nova localização (simplificado)
                    city_state = "Cidade/UF"  # Valor padrão
                    if " - " in location_str:
                        parts = location_str.split(" - ")
                        reference_point = parts[0]
                        city_state = parts[1] if len(parts) > 1 else city_state
                    else:
                        reference_point = location_str

                    if "/" in city_state:
                        city, state = city_state.split("/")
                    else:
                        city, state = city_state, "UF"

                    # Criar e retornar nova localização
                    return Location.objects.create(reference_point=reference_point, city=city, state=state)

            # Processar localizações
            pickup_location = get_or_create_location(pickup_location_str)
            if dropoff_location_str and dropoff_location_str != pickup_location_str:
                dropoff_location = get_or_create_location(dropoff_location_str)
            else:
                dropoff_location = pickup_location

            # Combinar data e hora
            pickup_datetime_str = f"{pickup_date} {pickup_time}"
            dropoff_datetime_str = f"{dropoff_date} {dropoff_time}"

            # Converter para objetos datetime
            try:
                pickup_datetime = datetime.strptime(pickup_datetime_str, "%Y-%m-%d %H:%M")
                dropoff_datetime = datetime.strptime(dropoff_datetime_str, "%Y-%m-%d %H:%M")
            except ValueError:
                messages.error(request, "Formato de data ou hora inválido.")
                return redirect("home")

            # Validar datas
            if dropoff_datetime <= pickup_datetime:
                messages.error(request, "A data/hora de devolução deve ser posterior à data/hora de retirada.")
                return redirect("home")

            if pickup_datetime < datetime.now():
                messages.error(request, "A data/hora de retirada não pode ser no passado.")
                return redirect("home")

            # Criar a reserva
            reservation = Reservation.objects.create(
                customer=user,  # Assumindo que o cliente é o próprio usuário
                vehicle=vehicle,
                pickup_location=pickup_location,
                dropoff_location=dropoff_location,
                pickup_datetime=pickup_datetime,
                dropoff_datetime=dropoff_datetime,
                created_at=datetime.now(),
            )

            # Atualizar status do veículo
            vehicle.status = "loaned"
            vehicle.save()

            # Notificar sucesso
            messages.success(request, f"Reserva do {vehicle.model} realizada com sucesso!")
            return redirect("home")  # Ou para uma página de confirmação

        except Vehicle.DoesNotExist:
            messages.error(request, "Veículo não encontrado.")
        except Exception as e:
            messages.error(request, f"Erro ao criar reserva: {str(e)}")

        return redirect("home")
    else:
        # Se não for POST, redirecionar para a home
        return redirect("home")


def search_vehicles(request):
    """
    View para buscar veículos via AJAX
    """
    query = request.GET.get("q", "")
    vehicles = []

    if query:
        # Buscar veículos que correspondam à consulta
        vehicle_results = Vehicle.objects.filter(
            models.Q(model__icontains=query) | models.Q(license_plate__icontains=query), status="available"
        )[
            :10
        ]  # Limitar a 10 resultados

        # Formatar resultados para JSON
        vehicles = [
            {
                "id": vehicle.id,
                "name": f"{vehicle.model} ({vehicle.license_plate})",
            }
            for vehicle in vehicle_results
        ]

    return JsonResponse({"vehicles": vehicles})
