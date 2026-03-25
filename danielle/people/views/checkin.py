import csv
from datetime import datetime

from django.conf import settings
from django.http import HttpResponse
from django.utils import timezone
from people.models import Checkin
from people.models import PatientCompanionCheckin
from people.serializers import CheckinSerializer
from people.serializers import PatientCompanionCheckinSerializer
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter,
    OpenApiExample,
    OpenApiResponse,
)

from people.constants import CHECKIN_CREATE_REQUEST_EXAMPLE, CHECKIN_RESPONSE_EXAMPLE


@extend_schema_view(
    list=extend_schema(
        description="Lista check-ins com filtros de atividade, busca por nome e ordenacao por data de criacao.",
        parameters=[
            OpenApiParameter(
                name="active",
                location=OpenApiParameter.QUERY,
                required=False,
                description="Filtra por status ativo do check-in.",
                examples=[
                    OpenApiExample("Ativos", value="true"),
                    OpenApiExample("Inativos", value="false"),
                ],
            ),
            OpenApiParameter(
                name="search",
                location=OpenApiParameter.QUERY,
                required=False,
                description="Busca por nome da pessoa principal.",
                examples=[OpenApiExample("Buscar por nome", value="Joao")],
            ),
            OpenApiParameter(
                name="ordering",
                location=OpenApiParameter.QUERY,
                required=False,
                description="Ordenacao por created_at. Use -created_at para descendente.",
            ),
        ],
        responses={
            200: CheckinSerializer(many=True),
            401: OpenApiResponse(description="Token invalido."),
        },
    ),
    create=extend_schema(
        description="Cria um check-in. Quando reason=patient, o campo companion e obrigatorio.",
        request=CheckinSerializer,
        examples=[
            OpenApiExample(
                "Exemplo de request",
                value=CHECKIN_CREATE_REQUEST_EXAMPLE,
                request_only=True,
            )
        ],
        responses={
            201: OpenApiResponse(
                response=CheckinSerializer,
                examples=[
                    OpenApiExample(
                        "Exemplo de resposta", value=CHECKIN_RESPONSE_EXAMPLE
                    )
                ],
            ),
            400: OpenApiResponse(description="Erro de validacao dos dados enviados."),
            401: OpenApiResponse(description="Token invalido."),
        },
    ),
    retrieve=extend_schema(description="Recupera os dados de um check-in por ID."),
    update=extend_schema(description="Atualiza totalmente os dados de um check-in."),
    partial_update=extend_schema(
        description="Atualiza parcialmente os dados de um check-in."
    ),
    destroy=extend_schema(description="Remove um check-in existente."),
)
class CheckinViewSet(viewsets.ModelViewSet):
    """API de gerenciamento de check-ins (entradas) da Casa de Apoio."""

    queryset = Checkin.objects.all()
    serializer_class = CheckinSerializer
    filter_backends = [
        filters.SearchFilter,
        DjangoFilterBackend,
        filters.OrderingFilter,
    ]
    search_fields = ["person__name"]
    filterset_fields = ["active"]
    ordering_fields = ["created_at"]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Checkin.objects.select_related("person", "companion")

    @extend_schema(
        description="Exporta check-ins em CSV para prestacao de contas. Respeita os mesmos filtros da listagem.",
        parameters=[
            OpenApiParameter(
                name="active",
                location=OpenApiParameter.QUERY,
                required=False,
                description="Filtra por status ativo do check-in.",
                examples=[
                    OpenApiExample("Ativos", value="true"),
                    OpenApiExample("Inativos", value="false"),
                ],
            ),
            OpenApiParameter(
                name="search",
                location=OpenApiParameter.QUERY,
                required=False,
                description="Busca por nome da pessoa principal.",
                examples=[OpenApiExample("Buscar por nome", value="Joao")],
            ),
            OpenApiParameter(
                name="ordering",
                location=OpenApiParameter.QUERY,
                required=False,
                description="Ordenacao por created_at. Use -created_at para descendente.",
            ),
        ],
        responses={
            200: OpenApiResponse(description="Arquivo CSV gerado com sucesso."),
            401: OpenApiResponse(description="Token invalido."),
            403: OpenApiResponse(
                description="Exportacao desabilitada por configuracao."
            ),
        },
    )
    @action(detail=False, methods=["get"], url_path="export-csv")
    def export_csv(self, request):
        if not getattr(settings, "EXPORT_REPORTS_ENABLED", False):
            return Response(
                {"detail": "Exportacao de relatorio desabilitada neste ambiente."},
                status=status.HTTP_403_FORBIDDEN,
            )

        queryset = self.filter_queryset(self.get_queryset())

        response = HttpResponse(content_type="text/csv; charset=utf-8")
        response["Content-Disposition"] = (
            f'attachment; filename="checkins-relatorio-{datetime.now().strftime("%Y%m%d%H%M%S")}.csv"'
        )

        writer = csv.writer(response)
        writer.writerow(
            [
                "id",
                "data_criacao",
                "pessoa",
                "acompanhante",
                "motivo",
                "ativo",
                "vaga_social",
                "numero_ca",
                "quimioterapia",
                "radioterapia",
                "cirurgia",
                "exames",
                "consulta",
                "outros",
            ]
        )

        for checkin in queryset:
            writer.writerow(
                [
                    checkin.id,
                    timezone.localtime(checkin.created_at).strftime("%d/%m/%Y %H:%M"),
                    checkin.person_name,
                    checkin.companion_name or "",
                    checkin.reason,
                    checkin.active,
                    checkin.social_vacancy,
                    checkin.ca_number or "",
                    checkin.chemotherapy,
                    checkin.radiotherapy,
                    checkin.surgery,
                    checkin.exams,
                    checkin.appointment,
                    checkin.other,
                ]
            )

        return response


@extend_schema_view(
    list=extend_schema(
        description="Lista check-ins simplificados de paciente com acompanhante.",
        parameters=[
            OpenApiParameter(
                name="search",
                location=OpenApiParameter.QUERY,
                required=False,
                description="Busca por nome do paciente.",
            ),
            OpenApiParameter(
                name="ordering",
                location=OpenApiParameter.QUERY,
                required=False,
                description="Ordenacao por created_at.",
            ),
        ],
    ),
    create=extend_schema(
        description="Cria check-in simplificado para vinculo paciente-acompanhante.",
        request=PatientCompanionCheckinSerializer,
    ),
    retrieve=extend_schema(description="Recupera check-in simplificado por ID."),
    update=extend_schema(
        description="Atualiza totalmente check-in simplificado por ID."
    ),
    partial_update=extend_schema(
        description="Atualiza parcialmente check-in simplificado por ID."
    ),
    destroy=extend_schema(description="Remove check-in simplificado por ID."),
)
class PatientCompanionCheckinViewSet(viewsets.ModelViewSet):
    """API para registros de paciente com acompanhante."""

    queryset = PatientCompanionCheckin.objects.all()
    serializer_class = PatientCompanionCheckinSerializer
    filter_backends = [
        filters.SearchFilter,
        DjangoFilterBackend,
        filters.OrderingFilter,
    ]
    search_fields = ["patient__name"]
    ordering_fields = ["created_at"]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PatientCompanionCheckin.objects.select_related("patient", "companion")
