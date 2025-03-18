from django.db import models

# Create your models here.

class Vehicle(models.Model):
    model = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    license_plate = models.CharField(max_length=20, unique=True)
    vin = models.CharField(max_length=17, unique=True, verbose_name="Numéro de Châssis")  # Ajout du VIN
    mileage = models.PositiveIntegerField()
    AVAILABILITY_CHOICES = [
        ('disponible', 'Disponible'),
        ('réservé', 'Réservé'),
        ('indisponible', 'Indisponible'),
    ]

    availability = models.CharField(
        max_length=15,
        choices=AVAILABILITY_CHOICES,
        default='disponible'
    )
    last_service_km = models.PositiveIntegerField()
    fuel_level = models.PositiveIntegerField(default=50, verbose_name="Niveau de Carburant")  # Ajout du niveau de carburant
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.brand} {self.model} ({self.license_plate})"