from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from people.models import Checkin, Checkout, HomeServices, Person


class DashboardViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="dashboard_user",
            email="dashboard@test.com",
            password="dashboard123",
        )

        self.person_1 = Person.objects.create(name="Pessoa Um")
        self.person_2 = Person.objects.create(name="Pessoa Dois")

        self.checkin_1 = Checkin.objects.create(
            person=self.person_1,
            reason="patient",
            active=True,
            chemotherapy=True,
        )
        self.checkin_2 = Checkin.objects.create(
            person=self.person_2,
            reason="professional",
            active=False,
        )

        Checkout.objects.create(checkin=self.checkin_2)

        HomeServices.objects.create(
            person=self.person_1,
            breakfast=True,
            lunch=True,
            dinner=True,
            shower=True,
            sleep=True,
        )
        HomeServices.objects.create(
            person=self.person_2,
            breakfast=False,
            lunch=True,
            snack=True,
            dinner=False,
            shower=False,
            sleep=False,
        )

    def test_dashboard_requires_authentication(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)

    def test_dashboard_returns_200_for_authenticated_user(self):
        self.client.login(username="dashboard_user", password="dashboard123")
        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dashboard.html")

    def test_dashboard_context_contains_expected_kpis(self):
        self.client.login(username="dashboard_user", password="dashboard123")
        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.context["total_checkins"], 2)
        self.assertEqual(response.context["total_checkouts"], 1)
        self.assertEqual(response.context["active_checkins"], 1)
        self.assertEqual(response.context["active_rate"], 50.0)

        services = {
            item["service"]: item["count"]
            for item in response.context["service_distribution"]
        }
        self.assertEqual(services["breakfast"], 1)
        self.assertEqual(services["lunch"], 2)
        self.assertEqual(services["snack"], 1)
        self.assertEqual(services["dinner"], 1)
        self.assertEqual(services["shower"], 1)
        self.assertEqual(services["sleep"], 1)
