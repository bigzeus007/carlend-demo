from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()

class Command(BaseCommand):
    help = "Ajoute des utilisateurs avec leurs groupes"

    def handle(self, *args, **kwargs):
        users_data = [
            {"username": "Aziz", "group": "Conseillers de service", "password": "123456", "email": "a.ibnekhyyat@superauto.ma"},
            {"username": "Badr", "group": "Conseillers de service", "password": "123456", "email": "m.baggari@superauto.ma"},
            {"username": "Abdelali", "group": "Conseillers de service", "password": "123456", "email": "a.amal@superauto.ma"},
            {"username": "Mohammed", "group": "Conseillers de service", "password": "123456", "email": "m.belmejdoub@superauto.ma"},
            {"username": "Bouabid", "group": "Validateurs", "password": "123456", "email": "b.elbadaoui@superauto.co.ma"},
            {"username": "Said", "group": "Admin", "password": "123456", "email": "s.tarhi@superauto.co.ma"},
            {"username": "Ismael", "group": "Guests", "password": "123456", "email": "i.ouladsayad@superauto.co.ma"},
            {"username": "Guest", "group": "Guests", "password": "123456", "email": "guest@superauto.ma"},
        ]

        for user_data in users_data:
            username = user_data["username"]
            email = user_data["email"]
            password = user_data["password"]
            group_name = user_data["group"]

            # Vérifier si l'utilisateur existe déjà
            if User.objects.filter(username=username).exists():
                self.stdout.write(self.style.WARNING(f"L'utilisateur {username} existe déjà."))
                continue

            # Créer l'utilisateur
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()

            # Ajouter l'utilisateur au bon groupe
            group, created = Group.objects.get_or_create(name=group_name)
            user.groups.add(group)

            self.stdout.write(self.style.SUCCESS(f"Utilisateur {username} ajouté au groupe {group_name}."))
