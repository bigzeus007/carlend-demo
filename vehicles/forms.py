from django import forms
from .models import Vehicle

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['brand', 'model', 'license_plate', 'vin', 'mileage', 'availability', 'last_service_km', 'fuel_level']  # Ajout des champs VIN et niveau de carburant
