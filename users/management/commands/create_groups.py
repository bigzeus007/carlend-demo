from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from vehicles.models import Vehicle
from reservations.models import Reservation
from historiques.models import Historique

class Command(BaseCommand):
    help = "Crée les groupes et définit les permissions"

    def handle(self, *args, **kwargs):
        # Création des groupes
        admin_group, created = Group.objects.get_or_create(name='Admin')
        service_advisor_group, created = Group.objects.get_or_create(name='Conseillers de service')
        validator_group, created = Group.objects.get_or_create(name='Validateurs')
        guest_group, created = Group.objects.get_or_create(name='Guests')

        # Liste des permissions
        all_permissions = Permission.objects.all()

        # Permissions pour l'Admin (Toutes les permissions)
        admin_group.permissions.set(all_permissions)

        # Permissions pour les Conseillers de service
        service_advisor_permissions = Permission.objects.filter(
            content_type__model__in=['reservation', 'historique']
        )
        service_advisor_group.permissions.set(service_advisor_permissions)

        # Permissions pour les Validateurs
        validator_permissions = Permission.objects.filter(
            content_type__model__in=['reservation', 'historique'],
            codename__in=['view_reservation', 'can_validate_reservation', 'view_historique']
        )
        validator_group.permissions.set(validator_permissions)

        # Permissions pour les Guests (visualisation uniquement)
        guest_permissions = Permission.objects.filter(
            content_type__model__in=['reservation', 'historique'],
            codename__in=['view_reservation', 'view_historique']
        )
        guest_group.permissions.set(guest_permissions)

        self.stdout.write(self.style.SUCCESS("Groupes et permissions créés avec succès"))
