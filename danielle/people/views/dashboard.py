from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.utils import timezone
from django.views.generic import TemplateView

from people.models import Checkin, Checkout, HomeServices


class DashboardView(LoginRequiredMixin, TemplateView):
    """Dashboard MVT com KPIs operacionais da Casa de Apoio."""

    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        total_checkins = Checkin.objects.count()
        total_checkouts = Checkout.objects.count()
        active_checkins = Checkin.objects.filter(active=True).count()

        services = HomeServices.objects.aggregate(
            breakfast=Count("id", filter=Q(breakfast=True)),
            lunch=Count("id", filter=Q(lunch=True)),
            snack=Count("id", filter=Q(snack=True)),
            dinner=Count("id", filter=Q(dinner=True)),
            shower=Count("id", filter=Q(shower=True)),
            sleep=Count("id", filter=Q(sleep=True)),
        )

        service_labels = {
            "breakfast": "Cafe da manha",
            "lunch": "Almoco",
            "snack": "Lanche da tarde",
            "dinner": "Jantar",
            "shower": "Banho",
            "sleep": "Pernoite",
        }

        service_distribution = [
            {
                "service": service,
                "label": service_labels[service],
                "count": count,
            }
            for service, count in services.items()
        ]

        active_rate = (
            round((active_checkins / total_checkins) * 100, 2) if total_checkins else 0
        )

        context.update(
            {
                "total_checkins": total_checkins,
                "total_checkouts": total_checkouts,
                "active_checkins": active_checkins,
                "active_rate": active_rate,
                "service_distribution": service_distribution,
                "updated_at": timezone.localtime(),
            }
        )
        return context
