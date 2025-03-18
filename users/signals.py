from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from users.models import User
from reservations.models import Reservation
from vehicles.models import Vehicle
from historiques.models import Historique

@receiver(post_migrate)
def create_user_groups(sender, **kwargs):
    if sender.name != "users":
        return

    # Création des groupes
    admin_group, _ = Group.objects.get_or_create(name="Admin")
    conseiller_group, _ = Group.objects.get_or_create(name="Conseillers de service")
    validateur_group, _ = Group.objects.get_or_create(name="Validateurs")
    guest_group, _ = Group.objects.get_or_create(name="Guests")

    # Permissions spécifiques aux réservations et véhicules
    reservation_ct = ContentType.objects.get_for_model(Reservation)
    vehicle_ct = ContentType.objects.get_for_model(Vehicle)
    historique_ct = ContentType.objects.get_for_model(Historique)

    permissions = {
        "Admin": Permission.objects.all(),
        "Conseillers de service": [
            Permission.objects.get(codename="add_reservation"),
            Permission.objects.get(codename="change_reservation"),
            Permission.objects.get(codename="view_reservation"),
            Permission.objects.get(codename="add_historique"),
            Permission.objects.get(codename="view_historique"),
        ],
        "Validateurs": [
            Permission.objects.get(codename="view_reservation"),
            Permission.objects.get(codename="can_validate_reservation"),
            Permission.objects.get(codename="view_historique"),
        ],
        "Guests": [
            Permission.objects.get(codename="view_reservation"),
            Permission.objects.get(codename="view_historique"),
        ],
    }

    # Assigner les permissions aux groupes
    for group_name, perms in permissions.items():
        group = Group.objects.get(name=group_name)
        group.permissions.set(perms)

