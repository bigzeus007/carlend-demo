from django.test import TestCase, Client
from django.urls import reverse
from reservations.models import Reservation
from vehicles.models import Vehicle
from django.contrib.auth.models import User

class ModelTests(TestCase):

    def setUp(self):
        self.vehicle = Vehicle.objects.create(
            brand="Toyota",
            model="Corolla",
            license_plate="ABC-123",
            mileage=15000,
            available=True
        )
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.reservation = Reservation.objects.create(
            vehicle=self.vehicle,
            user=self.user,
            start_date="2025-01-01",
            end_date="2025-01-05",
            status="pending"
        )

    def test_vehicle_creation(self):
        self.assertEqual(self.vehicle.brand, "Toyota")
        self.assertTrue(self.vehicle.available)

    def test_reservation_creation(self):
        self.assertEqual(self.reservation.status, "pending")
        self.assertEqual(self.reservation.vehicle, self.vehicle)


class ViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client.login(username="testuser", password="testpassword")
        self.vehicle = Vehicle.objects.create(
            brand="Toyota",
            model="Corolla",
            license_plate="ABC-123",
            mileage=15000,
            available=True
        )

    def test_reservation_list_view(self):
        response = self.client.get(reverse("reservations:list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "reservations/reservation_list.html")

    def test_add_reservation_view(self):
        response = self.client.post(reverse("reservations:add"), {
            "vehicle": self.vehicle.id,
            "start_date": "2025-01-01",
            "end_date": "2025-01-05",
            "status": "pending"
        })
        self.assertEqual(response.status_code, 302)  # Redirection après ajout


class IntegrationTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client.login(username="testuser", password="testpassword")
        self.vehicle = Vehicle.objects.create(
            brand="Toyota",
            model="Corolla",
            license_plate="ABC-123",
            mileage=15000,
            available=True
        )

    def test_reservation_workflow(self):
        # Ajouter une réservation
        response = self.client.post(reverse("reservations:add"), {
            "vehicle": self.vehicle.id,
            "start_date": "2025-01-01",
            "end_date": "2025-01-05",
            "status": "pending"
        })
        self.assertEqual(response.status_code, 302)

        # Vérifier que la réservation existe
        reservations = Reservation.objects.all()
        self.assertEqual(len(reservations), 1)
        self.assertEqual(reservations[0].status, "pending")
