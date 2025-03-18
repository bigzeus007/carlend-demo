from django.shortcuts import render, redirect, get_object_or_404
from .models import Reservation
from .forms import ReservationForm
from vehicles.models import Vehicle
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.http import HttpResponseForbidden

# Liste des réservations
def reservation_list(request):
    reservations = Reservation.objects.filter(is_active=True, is_assigned=False, deleted=False).order_by('-created_at')
    return render(request, 'reservations/reservation_list.html', {'reservations': reservations})

# Ajouter une réservation
@login_required
@permission_required('reservations.add_reservation', raise_exception=True)
def add_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST, request.FILES)  # Inclure les fichiers
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user  # Associer l'utilisateur connecté
            reservation.save()
            return redirect('reservation_list')
    else:
        form = ReservationForm()
    return render(request, 'reservations/add_reservation.html', {'form': form})

# Modifier une réservation
def edit_reservation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    if request.method == 'POST':
        form = ReservationForm(request.POST, request.FILES, instance=reservation)  # Inclure request.FILES
        if form.is_valid():
            # Vérifiez si de nouveaux fichiers ont été soumis
            
            form.save()
            return redirect('reservation_list')
    else:
        form = ReservationForm(instance=reservation)
    return render(request, 'reservations/edit_reservation.html', {'form': form})

# Afficher les details d'une réservation
def reservation_detail(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    return render(request, 'reservations/reservation_detail.html', {'reservation': reservation})
# Affecter un véhicule
def assign_vehicle(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    available_vehicles = Vehicle.objects.filter(availability='disponible')

    if request.method == 'POST':
        vehicle_id = request.POST.get('vehicle_id')
        vehicle = get_object_or_404(Vehicle, pk=vehicle_id)
        reservation.assigned_vehicle = vehicle
        reservation.is_assigned = True
        reservation.save()

        vehicle.availability = 'réservé'  # Marquer le véhicule comme réservé
        vehicle.save()

        return redirect('reservation_list')

    return render(request, 'reservations/assign_vehicle.html', {
        'reservation': reservation,
        'vehicles': available_vehicles,
    })

def reservation_history(request):
    reservations = Reservation.objects.filter(deleted=False).order_by('-reservation_date')
    return render(request, 'reservations/reservation_history.html', {
        'reservations': reservations,
    })

# Vérification que l'utilisateur est un validateur
def is_validator(user):
    return user.groups.filter(name='Validateur').exists()

@login_required
def archive_reservation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)

    if reservation.status_validation != 'rejected':
        messages.error(request, "Seules les réservations rejetées peuvent être archivées.")
        return redirect('reservation_list')

    reservation.deleted = True
    reservation.is_active = False
    reservation.save()
    messages.success(request, "Réservation archivée avec succès.")
    return redirect('reservation_list')

@login_required
@permission_required('reservations.can_validate_reservation', raise_exception=True)
def validate_reservation(request, pk):
    print(f"Utilisateur actuel: {request.user}")  # Vérifie qui est connecté
    if not request.user.is_authenticated:
        return HttpResponseForbidden("Vous devez être connecté pour valider une réservation.")

    if not request.user.has_perm('reservations.can_validate_reservation'):
        return HttpResponseForbidden("Vous n'avez pas la permission de valider cette réservation.")
    reservation = get_object_or_404(Reservation, pk=pk)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            reservation.status_validation = 'approved'
            messages.success(request, "Réservation validée avec succès.")
        elif action == 'reject':
            reservation.status_validation = 'rejected'
            messages.warning(request, "Réservation rejetée.")
        reservation.save()
        return redirect('reservation_list')

    return render(request, 'reservations/validate_reservation.html', {'reservation': reservation})