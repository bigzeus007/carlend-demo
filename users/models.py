from django.contrib.auth.models import AbstractUser, Group
from django.db import models

class User(AbstractUser):
    def is_admin(self):
        return self.groups.filter(name='Admin').exists()
    
    def is_conseiller(self):
        return self.groups.filter(name='Conseillers de service').exists()
    
    def is_validateur(self):
        return self.groups.filter(name='Validateurs').exists()
    
    def is_guest(self):
        return self.groups.filter(name='Guests').exists()
