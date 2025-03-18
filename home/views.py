from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from vehicles.models import Vehicle
from reservations.models import Reservation

@login_required
def home(request):
    # Comptage des véhicules disponibles
    available_vehicles_count = Vehicle.objects.filter(availability='disponible').count()
    
    # Comptage des véhicules indisponibles
    unavailable_vehicles_count = Vehicle.objects.filter(availability='indisponible').count()

    # Comptage des réservations en attente
    pending_reservations_count = Reservation.objects.filter(is_assigned=False, is_active=True).count()

    # Comptage des réservations actives (Réservé ou Livré)
    active_reservations_count = Vehicle.objects.filter(availability='réservé').count()

    # Passage des données au template
    return render(request, 'home/home.html', {
        'user': request.user,
        'available_vehicles_count': available_vehicles_count,
        'unavailable_vehicles_count': unavailable_vehicles_count,
        'pending_reservations_count': pending_reservations_count,
        'active_reservations_count': active_reservations_count,
    })