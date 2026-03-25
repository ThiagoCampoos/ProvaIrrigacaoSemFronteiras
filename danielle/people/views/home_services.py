from people.models import HomeServices
from people.serializers import HomeServicesSerializer
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter


@extend_schema_view(
    list=extend_schema(
        description='Lista servicos de apoio domestico com busca por nome da pessoa e ordenacao por data.',
        parameters=[
            OpenApiParameter(
                name='search',
                location=OpenApiParameter.QUERY,
                required=False,
                description='Busca por nome da pessoa atendida.',
            ),
            OpenApiParameter(
                name='ordering',
                location=OpenApiParameter.QUERY,
                required=False,
                description='Ordenacao por created_at.',
            ),
        ],
    ),
    create=extend_schema(description='Cria um registro de servicos domesticos para uma pessoa.'),
    retrieve=extend_schema(description='Recupera um registro de servicos domesticos por ID.'),
    update=extend_schema(description='Atualiza totalmente um registro de servicos domesticos.'),
    partial_update=extend_schema(description='Atualiza parcialmente um registro de servicos domesticos.'),
    destroy=extend_schema(description='Remove um registro de servicos domesticos.'),
)
class HomeServicesViewSet(viewsets.ModelViewSet):
    """API de servicos de apoio domestico da Casa de Apoio."""

    queryset = HomeServices.objects.all()
    serializer_class = HomeServicesSerializer
    filter_backends = [
        filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter
    ]
    search_fields = ['person__name']
    ordering_fields = ['created_at']
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return HomeServices.objects.select_related('person')