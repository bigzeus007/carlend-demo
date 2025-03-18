from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden, HttpResponse, JsonResponse
from django.contrib import messages
from reservations.models import Reservation
from vehicles.models import Vehicle
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import io


def parc_list(request):
    vehicles = Vehicle.objects.all()
    return render(request, 'parc/parc_list.html', {'vehicles': vehicles})

def parc_info(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)

    # Vérifier que le véhicule est "Indisponible" ou "Réservé"
    if vehicle.availability not in ['indisponible', 'réservé']:
        return HttpResponse("Vous ne pouvez consulter les informations que pour les véhicules indisponibles ou réservés.")

    reservation = Reservation.objects.filter(
        assigned_vehicle=vehicle,
        is_assigned=True
        ).first()
    context = {
        'vehicle': vehicle,
        'reservation': reservation,
        }
    return render(request, 'parc/parc_info.html', context)

def vehicle_info(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)

    context = {
        'vehicle': vehicle,
        }
    return render(request, 'parc/vehicle_info.html', context)

def parc_update(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    reservation = Reservation.objects.filter(assigned_vehicle=vehicle, is_assigned=True).first()
    available_vehicles = Vehicle.objects.filter(availability="disponible")

    if not reservation:
        return HttpResponse("Aucune réservation associée ou vous n'êtes pas le responsable de cette réservation.")
    
    if reservation.reservation_date and reservation.reservation_duration:
        calculated_return_date = reservation.reservation_date + timedelta(days=reservation.reservation_duration)
    else:
        calculated_return_date = reservation.end_date  # Valeur par défaut

    if request.method == 'POST':
        action = request.POST.get('action')  # Bouton cliqué
        if action == "update":
            # Enregistrer les modifications
            reservation.client_name = request.POST.get('client_name')
            reservation.criticality = request.POST.get('criticality')
            reservation.reasons = request.POST.get('reasons')
            new_vehicle_id = request.POST.get('assigned_vehicle')

            if new_vehicle_id and str(vehicle.pk) != new_vehicle_id:
                # Libérer l'ancien véhicule
                vehicle.availability = "disponible"
                vehicle.save()

                # Assigner un nouveau véhicule
                new_vehicle = get_object_or_404(Vehicle, pk=new_vehicle_id)
                reservation.assigned_vehicle = new_vehicle
                new_vehicle.availability = "réservé"
                new_vehicle.save()

            # Récupérer et valider la date de retour
            return_date = request.POST.get('return_date')
            if return_date:  # Vérifiez que la date est fournie
                try:
                    reservation.end_date = datetime.strptime(return_date, '%Y-%m-%d').date()
                except ValueError:
                    messages.error(request, "Le format de la date est invalide.")
                    return redirect('parc_update', pk=pk)
            # Gestion conditionnelle des fichiers
            if request.FILES.get('driving_license_front'):
                reservation.driving_license_front = request.FILES.get('driving_license_front')
            if request.FILES.get('driving_license_back'):
                reservation.driving_license_back = request.FILES.get('driving_license_back')
            if request.FILES.get('id_card_front'):
                reservation.id_card_front = request.FILES.get('id_card_front')
            if request.FILES.get('id_card_back'):
                reservation.id_card_back = request.FILES.get('id_card_back')
            reservation.save()
            messages.success(request, "Réservation mise à jour avec succès.")
            return redirect('parc_list')

        elif action == "confirm_delivery":
            # Confirmer la livraison
            # Confirmer la livraison avec gestion conditionnelle des fichiers
            if request.FILES.get('driving_license_front'):
                reservation.driving_license_front = request.FILES.get('driving_license_front')
            if request.FILES.get('driving_license_back'):
                reservation.driving_license_back = request.FILES.get('driving_license_back')
            if request.FILES.get('id_card_front'):
                reservation.id_card_front = request.FILES.get('id_card_front')
            if request.FILES.get('id_card_back'):
                reservation.id_card_back = request.FILES.get('id_card_back')
            vehicle.availability = "indisponible"
            reservation.start_date = datetime.now()
            reservation.save()
            vehicle.save()
            messages.success(request, "Livraison confirmée.")
            return redirect('parc_list')

        elif action == "confirm_return":
            # Confirmer le retour
            # Confirmer le retour avec gestion conditionnelle des fichiers
            if request.FILES.get('driving_license_front'):
                reservation.driving_license_front = request.FILES.get('driving_license_front')
            if request.FILES.get('driving_license_back'):
                reservation.driving_license_back = request.FILES.get('driving_license_back')
            if request.FILES.get('id_card_front'):
                reservation.id_card_front = request.FILES.get('id_card_front')
            if request.FILES.get('id_card_back'):
                reservation.id_card_back = request.FILES.get('id_card_back')
            vehicle.availability = "disponible"
            reservation.end_date = datetime.now()
            reservation.is_assigned = False
            reservation.is_active = False
            reservation.save()
            vehicle.save()
            messages.success(request, "Retour confirmé.")
            return redirect('parc_list')

        elif action == "cancel_reservation":
            # Annuler la réservation
            cancellation_reason = request.POST.get('cancellation_reason')
    
            if reservation.assigned_vehicle:
                reservation.assigned_vehicle.availability = "disponible"
                reservation.assigned_vehicle.save()  # Libérer le véhicule

            reservation.deleted = True
            reservation.is_assigned = False
            reservation.is_active = False
            reservation.assigned_vehicle = None  # Supprimer l'association du véhicule
            reservation.reasons = f"Annulé : {cancellation_reason}" if cancellation_reason else "Annulé"
            
            reservation.save()
            # Nettoyer la session après annulation
            request.session.pop('reservation_data', None)
            
            messages.success(request, "Réservation annulée.")
            return redirect('parc_list')

    context = {
        'vehicle': vehicle,
        'reservation': reservation,
        'available_vehicles': available_vehicles,
        'calculated_return_date': calculated_return_date.strftime('%Y-%m-%d') if calculated_return_date else "",
    }
    return render(request, 'parc/parc_update.html', context)

def confirm_return_update(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    reservation = Reservation.objects.filter(assigned_vehicle=vehicle, is_assigned=True).first()

    if not reservation:
        return HttpResponse("Aucune réservation associée pour ce véhicule.")

    if request.method == 'POST':
        # Récupération des données du formulaire
        new_mileage = int(request.POST.get('mileage', vehicle.mileage))
        new_fuel_level = int(request.POST.get('fuel_level', vehicle.fuel_level))

        # Vérification que le nouveau kilométrage est valide
        if new_mileage < vehicle.mileage:
            messages.error(request, "Le nouveau kilométrage ne peut pas être inférieur à l'ancien.")
            return render(request, 'parc/confirm_return_update.html', {'vehicle': vehicle})

        # Mise à jour des informations du véhicule
        vehicle.mileage = new_mileage
        vehicle.fuel_level = new_fuel_level
        vehicle.availability = "disponible"
        vehicle.save()

        # Mise à jour de la réservation
        reservation.end_date = datetime.now()
        reservation.is_assigned = False
        reservation.is_active = False
        reservation.save()

        messages.success(request, "Retour confirmé avec mise à jour des données.")
        return redirect('parc_list')

    return render(request, 'parc/confirm_return_update.html', {'vehicle': vehicle})


def update_vehicle_status(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    reservation = Reservation.objects.filter(assigned_vehicle=vehicle, is_assigned=True).first()

    if request.method == 'POST':
        # Récupération des données du formulaire
        client_name = request.POST.get('client_name')
        criticality = request.POST.get('criticality')
        new_vehicle_id = request.POST.get('new_vehicle')
        reasons = request.POST.get('reasons')
        status = request.POST.get('status')
        delivery_date = request.POST.get('delivery_date')

        if client_name:
            reservation.client_name = client_name
        if criticality:
            reservation.criticality = criticality
        if new_vehicle_id and new_vehicle_id != str(vehicle.id):
            new_vehicle = get_object_or_404(Vehicle, pk=new_vehicle_id)
            reservation.assigned_vehicle = new_vehicle
            new_vehicle.availability = 'Réservé'
            new_vehicle.save()
            vehicle.availability = 'disponible'
        if reasons:
            reservation.reasons = reasons
        if status == 'livré':
            delivery_date = request.POST.get('delivery_date')
            if delivery_date:
                try:
                    reservation.start_date = datetime.strptime(delivery_date, '%Y-%m-%d').date()
                    vehicle.availability = 'indisponible'
                except ValueError:
                    messages.error(request, "Le format de la date de livraison est invalide.")
                    return redirect('update_vehicle_status', pk=pk)

        elif status == 'annulé':
            reservation.deleted = True
            vehicle.availability = 'disponible'

        reservation.save()
        vehicle.save()
        return redirect('parc_list')

    available_vehicles = Vehicle.objects.filter(availability='disponible')

    context = {
        'vehicle': vehicle,
        'reservation': reservation,
        'available_vehicles': available_vehicles,
    }
    return render(request, 'parc/update_vehicle.html', context)

def generate_contract(request, pk):
    # Récupérer la réservation associée au véhicule
    reservation = get_object_or_404(Reservation, assigned_vehicle_id=pk, is_assigned=True)

    # Créer un buffer en mémoire pour stocker le PDF
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)

    # Contenu du contrat
    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, 800, "CONTRAT DE PRÊT DE VÉHICULE")

    p.setFont("Helvetica", 12)
    p.drawString(100, 760, "Super Auto Distribution (S.A.D)")
    p.drawString(100, 740, "Lot 38 ZI VITA route de Casablanca, RABAT")

    p.drawString(100, 700, f"Nom du client : {reservation.client_name}")
    p.drawString(100, 680, f"Numéro CIN : ___________")  # Ajouter le champ CIN si disponible
    p.drawString(100, 660, f"Modèle du véhicule : {reservation.assigned_vehicle.model}")
    p.drawString(100, 640, f"Immatriculation : {reservation.client_license_plate}")

    p.drawString(100, 620, f"Date de début : {reservation.start_date}")
    p.drawString(100, 600, f"Date de retour prévue : {reservation.end_date}")

    p.drawString(100, 550, "Le bénéficiaire s'engage à restituer le véhicule dans le même état.")
    p.drawString(100, 530, "Toute détérioration sera à sa charge.")

    p.drawString(100, 500, "Fait à Rabat, le __/__/____")
    p.drawString(100, 470, "Signature du bénéficiaire : ____________________")
    p.drawString(350, 470, "Signature de S.A.D : ____________________")

    # Finaliser le PDF
    p.showPage()
    p.save()

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="contrat.pdf"'
    return response
