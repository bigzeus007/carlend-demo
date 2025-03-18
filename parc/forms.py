from django import forms
from .models import Reservation

class UpdateReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['client_name', 'status', 'end_date', 'reasons']
