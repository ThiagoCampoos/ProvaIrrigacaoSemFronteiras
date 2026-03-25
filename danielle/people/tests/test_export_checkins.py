import csv
import io

from django.contrib.auth import get_user_model
from django.test import override_settings
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from people.models import Checkin, Person


class ExportCheckinsTests(APITestCase):
    def setUp(self):
        user_model = get_user_model()
        self.user = user_model.objects.create_user(
            username="test_export",
            email="test_export@test.com",
            password="test",
        )
        self.token = Token.objects.create(user=self.user)

        self.person_1 = Person.objects.create(name="Maria da Silva")
        self.person_2 = Person.objects.create(name="Joao Pereira")

        Checkin.objects.create(person=self.person_1, reason="professional", active=True)
        Checkin.objects.create(
            person=self.person_2, reason="professional", active=False
        )

        self.url = "/api/v1/checkins/export-csv/"

    def _auth(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

    def test_export_csv_requires_authentication(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @override_settings(EXPORT_REPORTS_ENABLED=False)
    def test_export_csv_returns_403_when_feature_flag_is_disabled(self):
        self._auth()

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @override_settings(EXPORT_REPORTS_ENABLED=True)
    def test_export_csv_returns_file_when_feature_flag_is_enabled(self):
        self._auth()

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(
            'attachment; filename="checkins-relatorio-', response["Content-Disposition"]
        )
        self.assertTrue(response["Content-Type"].startswith("text/csv"))

        rows = list(csv.reader(io.StringIO(response.content.decode("utf-8"))))
        self.assertEqual(rows[0][0], "id")
        self.assertEqual(len(rows), 3)

    @override_settings(EXPORT_REPORTS_ENABLED=True)
    def test_export_csv_applies_active_filter(self):
        self._auth()

        response = self.client.get(self.url, {"active": "true"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        rows = list(csv.reader(io.StringIO(response.content.decode("utf-8"))))
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[1][2], "Maria da Silva")

    @override_settings(EXPORT_REPORTS_ENABLED=True)
    def test_export_csv_applies_search_filter(self):
        self._auth()

        response = self.client.get(self.url, {"search": "Joao"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        rows = list(csv.reader(io.StringIO(response.content.decode("utf-8"))))
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[1][2], "Joao Pereira")
