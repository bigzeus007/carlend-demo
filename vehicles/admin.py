from django.contrib import admin

# Register your models here.
from .models import Vehicle

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'license_plate', 'availability', 'mileage', 'last_service_km')
    search_fields = ('brand', 'model', 'license_plate')