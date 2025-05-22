import traceback  # Para capturar traceback completo
from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import models
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import now  # Melhor que datetime.now() para timezone-aware
from django.utils.timezone import localtime, make_aware

from customer.models import Customer  # Adicionar esta importação

from .models import Location, Reservation, Vehicle

# Create your views here.


@login_required
def create_reservation(request):
    if request.method == "POST":
        try:
            print(">> Requisição POST recebida para criar reserva.")
            user = request.user
            print(f">> Usuário autenticado: {user}")
            # Obter o perfil Customer associado ao User logado
            try:
                customer_profile = Customer.objects.get(user_id=user)
            except Customer.DoesNotExist:
                messages.error(request, "Perfil de cliente não encontrado. Por favor, complete seu perfil.")
                print(f"!! Perfil Customer não encontrado para o usuário: {user}")
                # Você pode redirecionar para uma página de criação/atualização de perfil aqui
                return redirect("home")  # Ou para 'update_customer_profile' se tiver essa URL
            print(f">> Perfil Customer encontrado: {customer_profile}")

            vehicle_id = request.POST.get("vehicle_id")
            pickup_location_id = request.POST.get("pickup_location")
            dropoff_location_id = request.POST.get("dropoff_location")
            pickup_date = request.POST.get("pickup_date")
            pickup_time = request.POST.get("pickup_time")
            dropoff_date = request.POST.get("dropoff_date")
            dropoff_time = request.POST.get("dropoff_time")

            print(
                ">> Dados recebidos:",
                vehicle_id,
                pickup_location_id,
                dropoff_location_id,
                pickup_date,
                pickup_time,
                dropoff_date,
                dropoff_time,
            )

            if not all([vehicle_id, pickup_location_id, pickup_date, pickup_time, dropoff_date, dropoff_time]):
                messages.error(request, "Todos os campos obrigatórios devem ser preenchidos.")
                print("!! Campos obrigatórios faltando.")
                return redirect("home")

            vehicle = get_object_or_404(Vehicle, pk=vehicle_id)
            print(f">> Veículo encontrado: {vehicle}")

            if vehicle.status != "available":
                messages.error(request, "Este veículo não está mais disponível para reserva.")
                print(f"!! Veículo com status '{vehicle.status}' (esperado: 'available').")
                return redirect("home")

            pickup_location = get_object_or_404(Location, pk=pickup_location_id)
            print(f">> Local de retirada encontrado: {pickup_location}")

            dropoff_location = (
                get_object_or_404(Location, pk=dropoff_location_id)
                if dropoff_location_id and dropoff_location_id != pickup_location_id
                else pickup_location
            )
            print(f">> Local de devolução encontrado: {dropoff_location}")

            pickup_datetime_str = f"{pickup_date} {pickup_time}"
            dropoff_datetime_str = f"{dropoff_date} {dropoff_time}"

            print(">> Datas combinadas:", pickup_datetime_str, dropoff_datetime_str)

            pickup_datetime = make_aware(datetime.strptime(pickup_datetime_str, "%Y-%m-%d %H:%M"))
            dropoff_datetime = make_aware(datetime.strptime(dropoff_datetime_str, "%Y-%m-%d %H:%M"))

            if dropoff_datetime <= pickup_datetime:
                messages.error(request, "A data/hora de devolução deve ser posterior à data/hora de retirada.")
                print("!! dropoff_datetime <= pickup_datetime")
                return redirect("home")

            if pickup_datetime.date() < localtime(now()).date():
                messages.error(request, "A data de retirada não pode ser anterior à data de hoje.")
                print("!! pickup_datetime.date() < hoje")
                return redirect("home")
            print(">> Criando reserva...")
            reservation = Reservation.objects.create(
                customer=customer_profile,  # Verifique se o modelo espera User ou Customer
                vehicle=vehicle,
                pickup_location=pickup_location,
                dropoff_location=dropoff_location,
                pickup_datetime=pickup_datetime,
                dropoff_datetime=dropoff_datetime,
                created_at=now(),
            )
            print(f">> Reserva criada com sucesso: {reservation}")

            vehicle.status = "loaned"
            vehicle.save()
            print(f">> Status do veículo atualizado para 'loaned'.")

            messages.success(request, f"Reserva do {vehicle.model} realizada com sucesso!")
            return redirect("reservation_detail", reservation_id=reservation.id)  # ALTERADO AQUI

        except Vehicle.DoesNotExist:
            messages.error(request, "Veículo não encontrado.")
            print("!! Exceção: Vehicle.DoesNotExist")
        except Exception as e:
            traceback.print_exc()
            messages.error(request, f"Erro ao criar reserva: {str(e)}")
            print("!! Erro inesperado:", str(e))

        return redirect("home")
    else:
        print(">> Requisição GET recebida, redirecionando.")
        return redirect("home")


@login_required
def reservation_detail(request, reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id)

    # Verificar permissão:
    # O usuário logado deve ser o cliente da reserva OU um staff/admin.
    is_owner = reservation.customer.user_id == request.user
    is_staff_user = request.user.is_staff

    if not (is_owner or is_staff_user):
        messages.error(request, "Você não tem permissão para visualizar esta reserva.")
        return redirect("home")  # Ou return HttpResponseForbidden("Você não tem permissão para ver esta reserva.")

    context = {"reservation": reservation}
    return render(request, "reservation/reservation_detail.html", context)


@login_required
def my_reservations(request):
    user = request.user
    customer_profile = None
    reservations_list = []

    # Tenta obter o perfil de cliente do usuário logado
    try:
        customer_profile = Customer.objects.get(user_id=user)
    except Customer.DoesNotExist:
        messages.error(
            request, "Perfil de cliente não encontrado. Por favor, complete seu perfil para ver suas reservas."
        )
        return redirect("home")  # Ou para a página de criação/atualização de perfil

    if customer_profile:
        # Busca todas as reservas associadas a este perfil de cliente
        # Ordena pelas mais recentes primeiro (data de criação ou data de retirada)
        reservations_list = Reservation.objects.filter(customer=customer_profile).order_by("-created_at")

    context = {
        "reservations": reservations_list,
    }

    return render(request, "reservation/my_reservations.html", context)


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
