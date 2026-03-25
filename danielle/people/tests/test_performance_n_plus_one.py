from django.contrib.admin.sites import AdminSite
from django.test import RequestFactory, TestCase

from people.admin import (
    CheckinAdmin,
    CheckoutAdmin,
    HomeServicesAdmin,
    ProfessionalServicesAdmin,
)
from people.models import Checkin, Checkout, HomeServices, ProfessionalServices
from people.views import (
    CheckinViewSet,
    HomeServicesViewSet,
    ProfessionalServicesViewSet,
)
from people.views.checkin import PatientCompanionCheckinViewSet


class QuerysetOptimizationTests(TestCase):
    def test_checkin_viewset_uses_select_related(self):
        qs = CheckinViewSet().get_queryset()
        self.assertIn("person", qs.query.select_related)
        self.assertIn("companion", qs.query.select_related)

    def test_patient_companion_viewset_uses_select_related(self):
        qs = PatientCompanionCheckinViewSet().get_queryset()
        self.assertIn("patient", qs.query.select_related)
        self.assertIn("companion", qs.query.select_related)

    def test_home_services_viewset_uses_select_related(self):
        qs = HomeServicesViewSet().get_queryset()
        self.assertIn("person", qs.query.select_related)

    def test_professional_services_viewset_uses_select_related(self):
        qs = ProfessionalServicesViewSet().get_queryset()
        self.assertIn("professional", qs.query.select_related)


class AdminOptimizationTests(TestCase):
    def setUp(self):
        self.request = RequestFactory().get("/admin/people/")
        self.admin_site = AdminSite()

    def test_checkin_admin_search_field_is_related_name(self):
        admin_instance = CheckinAdmin(Checkin, self.admin_site)
        self.assertIn("person__name", admin_instance.search_fields)

    def test_checkout_admin_queryset_uses_select_related_chain(self):
        admin_instance = CheckoutAdmin(Checkout, self.admin_site)
        qs = admin_instance.get_queryset(self.request)
        self.assertIn("checkin", qs.query.select_related)
        self.assertIn("person", qs.query.select_related["checkin"])

    def test_home_services_admin_has_list_select_related(self):
        admin_instance = HomeServicesAdmin(HomeServices, self.admin_site)
        self.assertIn("person", admin_instance.list_select_related)

    def test_professional_services_admin_has_list_select_related(self):
        admin_instance = ProfessionalServicesAdmin(
            ProfessionalServices, self.admin_site
        )
        self.assertIn("professional", admin_instance.list_select_related)
