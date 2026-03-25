from people.models import ProfessionalServices
from people.serializers import ProfessionalServicesSerializer
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter


@extend_schema_view(
    list=extend_schema(
        description='Lista servicos profissionais com busca por nome do profissional e ordenacao por data.',
        parameters=[
            OpenApiParameter(
                name='search',
                location=OpenApiParameter.QUERY,
                required=False,
                description='Busca por nome do profissional.',
            ),
            OpenApiParameter(
                name='ordering',
                location=OpenApiParameter.QUERY,
                required=False,
                description='Ordenacao por created_at.',
            ),
        ],
    ),
    create=extend_schema(description='Cria um registro de servico profissional.'),
    retrieve=extend_schema(description='Recupera um registro de servico profissional por ID.'),
    update=extend_schema(description='Atualiza totalmente um registro de servico profissional.'),
    partial_update=extend_schema(description='Atualiza parcialmente um registro de servico profissional.'),
    destroy=extend_schema(description='Remove um registro de servico profissional.'),
)
class ProfessionalServicesViewSet(viewsets.ModelViewSet):
    """API de servicos profissionais associados a pessoas e atendimentos."""

    queryset = ProfessionalServices.objects.all()
    serializer_class = ProfessionalServicesSerializer
    filter_backends = [
        filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter
    ]
    search_fields = ['professional__name']
    ordering_fields = ['created_at']
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ProfessionalServices.objects.select_related('professional')