from django.core.management import call_command
from django.test import TestCase

from people.models import (
    Checkin,
    Checkout,
    HomeServices,
    PatientCompanionCheckin,
    Person,
    ProfessionalServices,
)


class SeedDbCommandTests(TestCase):
    def test_seed_db_creates_consistent_data(self):
        call_command(
            "seed_db",
            people=20,
            checkins=14,
            home_services=12,
            professional_services=8,
            checkout_rate=0.30,
            seed=123,
            clear=True,
            verbosity=0,
        )

        self.assertEqual(Person.objects.count(), 20)
        self.assertEqual(Checkin.objects.count(), 14)
        self.assertEqual(HomeServices.objects.count(), 12)
        self.assertEqual(ProfessionalServices.objects.count(), 8)
        self.assertEqual(Checkout.objects.count(), 4)

        patient_checkins = Checkin.objects.filter(reason="patient")
        self.assertFalse(patient_checkins.filter(companion__isnull=True).exists())
        self.assertEqual(
            PatientCompanionCheckin.objects.count(), patient_checkins.count()
        )

        checked_out_ids = set(Checkout.objects.values_list("checkin_id", flat=True))
        inactive_ids = set(
            Checkin.objects.filter(active=False).values_list("id", flat=True)
        )
        self.assertSetEqual(inactive_ids, checked_out_ids)

    def test_seed_db_is_repeatable_with_same_seed(self):
        self._run_seed(seed=77)
        first_snapshot = self._snapshot()

        self._run_seed(seed=77)
        second_snapshot = self._snapshot()

        self.assertEqual(first_snapshot, second_snapshot)

    def test_seed_db_produces_different_snapshot_with_different_seed(self):
        self._run_seed(seed=77)
        first_snapshot = self._snapshot()

        self._run_seed(seed=78)
        second_snapshot = self._snapshot()

        self.assertNotEqual(first_snapshot, second_snapshot)

    def test_seed_db_clamps_negative_counts_and_checkout_rate(self):
        call_command(
            "seed_db",
            people=-8,
            checkins=-7,
            home_services=-2,
            professional_services=-4,
            checkout_rate=4.2,
            seed=200,
            clear=True,
            verbosity=0,
        )

        self.assertEqual(Person.objects.count(), 1)
        self.assertEqual(Checkin.objects.count(), 0)
        self.assertEqual(HomeServices.objects.count(), 0)
        self.assertEqual(ProfessionalServices.objects.count(), 0)
        self.assertEqual(Checkout.objects.count(), 0)

    def test_seed_db_defaults_generate_expected_volume(self):
        call_command("seed_db", clear=True, verbosity=0)

        self.assertEqual(Person.objects.count(), 120)
        self.assertEqual(Checkin.objects.count(), 90)
        self.assertEqual(HomeServices.objects.count(), 75)
        self.assertEqual(ProfessionalServices.objects.count(), 40)
        expected_checkouts = int(round(90 * 0.35))
        self.assertEqual(Checkout.objects.count(), expected_checkouts)

    def _run_seed(self, seed):
        call_command(
            "seed_db",
            people=10,
            checkins=7,
            home_services=5,
            professional_services=4,
            checkout_rate=0.40,
            seed=seed,
            clear=True,
            verbosity=0,
        )

    def _snapshot(self):
        people = list(
            Person.objects.order_by("id").values_list(
                "name",
                "mother_name",
                "cpf",
                "city",
                "state",
                "postal_code",
            )
        )
        checkins = list(
            Checkin.objects.order_by("id").values_list(
                "person__cpf",
                "reason",
                "companion__cpf",
                "active",
            )
        )
        home_services = list(
            HomeServices.objects.order_by("id").values_list(
                "person__cpf",
                "breakfast",
                "lunch",
                "snack",
                "dinner",
                "shower",
                "sleep",
            )
        )
        professional_services = list(
            ProfessionalServices.objects.order_by("id").values_list(
                "professional__cpf",
                "title",
            )
        )

        return {
            "people": people,
            "checkins": checkins,
            "home_services": home_services,
            "professional_services": professional_services,
            "checkouts": Checkout.objects.count(),
        }


class SeedLocalCommandTests(TestCase):
    def test_seed_local_runs_with_defaults(self):
        call_command("seed_local", verbosity=0)

        self.assertEqual(Person.objects.count(), 120)
        self.assertEqual(Checkin.objects.count(), 90)
        self.assertEqual(HomeServices.objects.count(), 75)
        self.assertEqual(ProfessionalServices.objects.count(), 40)

    def test_seed_local_no_clear_keeps_existing_data(self):
        call_command(
            "seed_db",
            people=3,
            checkins=2,
            home_services=2,
            professional_services=1,
            clear=True,
            seed=90,
            verbosity=0,
        )

        call_command(
            "seed_local",
            clear=False,
            people=2,
            checkins=1,
            home_services=1,
            professional_services=1,
            seed=91,
            verbosity=0,
        )

        self.assertEqual(Person.objects.count(), 5)
        self.assertEqual(Checkin.objects.count(), 3)
        self.assertEqual(HomeServices.objects.count(), 3)
        self.assertEqual(ProfessionalServices.objects.count(), 2)
