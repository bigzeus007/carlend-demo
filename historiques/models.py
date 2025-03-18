from django.db import models
from reservations.models import Reservation
from vehicles.models import Vehicle

class Historique(models.Model):
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE, related_name='historique')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    vehicle = models.ForeignKey(Vehicle, null=True, blank=True, on_delete=models.SET_NULL)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    distance_travelled = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Historique de {self.reservation.client_name}"
