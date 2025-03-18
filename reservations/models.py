from django.db import models
from cloudinary.models import CloudinaryField
from vehicles.models import Vehicle  
from django.conf import settings

class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'En attente de validation'),
        ('approved', 'Validée'),
        ('rejected', 'Rejetée'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE, related_name='reservations')
    client_name = models.CharField(max_length=100,verbose_name="Nom Client")
    client_license_plate = models.CharField(max_length=20,verbose_name="Plaque")
    client_vehicle_date = models.DateField(verbose_name="Mise en circulation")
    commercial_advisor = models.CharField(max_length=100,verbose_name="Nom Commercial")
    service_advisor = models.CharField(max_length=100,verbose_name="Nom conseiller de service")
    criticality = models.CharField(max_length=20,verbose_name="Criticité", choices=[('low', 'Faible'), ('medium', 'Moyen'), ('high', 'Critique')])
    reservation_date = models.DateField(verbose_name="Date de réservation")
    reservation_duration = models.PositiveIntegerField(verbose_name="Durée de la réservation", help_text="en jours")
    reasons = models.TextField()
    assigned_vehicle = models.ForeignKey(Vehicle, null=True, blank=True, on_delete=models.SET_NULL)
    is_assigned = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)  
    start_date = models.DateField(null=True, blank=True)  
    end_date = models.DateField(null=True, blank=True)  
    deleted = models.BooleanField(default=False)  
    driving_license_front = CloudinaryField('image', null=True, blank=True)
    driving_license_back = CloudinaryField('image', null=True, blank=True)
    id_card_front = CloudinaryField('image', null=True, blank=True)
    id_card_back = CloudinaryField('image', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status_validation = models.CharField(
        max_length=10, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="Statut de validation"
    )
    class Meta:
        permissions = [
            ("can_validate_reservation", "Peut valider les réservations"),
        ]

    def __str__(self):
        return f"{self.client_name} - {self.reservation_date} ({self.get_status_validation_display()})"
