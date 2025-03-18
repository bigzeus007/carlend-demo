from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User  # Import du modèle personnalisé

admin.site.register(User, UserAdmin)  # Ajout dans l'interface admin
