from django.shortcuts import render, redirect
from django.db.models import Q
from reservations.models import Reservation

def historique_pret(request):
    search_date = request.GET.get('search_date')  # Récupérer la date de recherche
    reservations = Reservation.objects.filter(
        is_assigned=False,  # Non assignées car retournées
        start_date__isnull=False,
        end_date__isnull=False
    )

    if search_date:  # Si une date est saisie
        reservations = reservations.filter(
            Q(start_date__lte=search_date) & Q(end_date__gte=search_date)
        )

    reservations = reservations.order_by('-end_date')  # Tri par date de retour
    return render(request, 'historiques/historique_list.html', {
        'reservations': reservations,
        'historique_type': 'pret',
    })

def historique_index(request):
    # Redirige automatiquement vers l'historique des prêts par défaut
    return redirect('historique_pret')

def historique_annulation(request):
    annulations = Reservation.objects.filter(
        deleted=True  # Réservations annulées
    ).order_by('-modified_date')  # Tri par date d'annulation
    return render(request, 'historiques/historique_list.html', {
        'reservations': annulations,
        'historique_type': 'annulation',
    })
