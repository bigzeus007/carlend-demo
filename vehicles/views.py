from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from .models import Vehicle
from .forms import VehicleForm
# Create your views here.

def index(request):
    return HttpResponse("Bienvenue sur la gestion des véhicules de CarLend!")

@staff_member_required
def vehicle_list(request):
    vehicles = Vehicle.objects.all()
    return render(request, 'vehicles/vehicle_list.html', {'vehicles': vehicles})

@staff_member_required
def add_vehicle(request):
    form = VehicleForm()  # Initialise le formulaire AVANT le test de la méthode

    if request.method == 'POST':
        print("Données POST reçues :", request.POST)  # Debugging
        form = VehicleForm(request.POST)

        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.fuel_level = int(request.POST.get('fuel_level', 50))  # Assure une conversion propre
            vehicle.availability = request.POST.get('availability', 'disponible')
            vehicle.save()
            print("Véhicule enregistré avec succès !")
            return redirect('vehicle_list')  
        else:
            print("Erreurs du formulaire :", form.errors)  # Debugging des erreurs

    return render(request, 'vehicles/add_vehicle.html', {'form': form})


@staff_member_required
def edit_vehicle(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    if request.method == 'POST':
        form = VehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.fuel_level = int(request.POST.get('fuel_level', vehicle.fuel_level))  # Assure la conversion en entier
            vehicle.save()
            return redirect('vehicle_list')
    else:
        form = VehicleForm(instance=vehicle)
    return render(request, 'vehicles/edit_vehicle.html', {'form': form})

@staff_member_required
def delete_vehicle(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    vehicle.delete()
    return redirect('vehicle_list')