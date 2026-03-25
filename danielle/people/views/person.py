from people.models import Person
from people.serializers import PersonSerializer
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiExample, OpenApiResponse

from people.constants import PEOPLE_RESPONSE_EXAMPLE, PEOPLE_CREATE_REQUEST_EXAMPLE


@extend_schema_view(
    list=extend_schema(
        description='Lista pessoas com suporte a busca, ordenacao e paginacao.',
        parameters=[
            OpenApiParameter(
                name='search',
                location=OpenApiParameter.QUERY,
                required=False,
                description='Busca textual por nome da pessoa.',
                examples=[OpenApiExample('Buscar por nome', value='Joao')],
            ),
            OpenApiParameter(
                name='ordering',
                location=OpenApiParameter.QUERY,
                required=False,
                description='Ordenacao por name. Use -name para descendente.',
                examples=[OpenApiExample('Ascendente', value='name'), OpenApiExample('Descendente', value='-name')],
            ),
            OpenApiParameter(name='limit', location=OpenApiParameter.QUERY, required=False, type=int),
            OpenApiParameter(name='offset', location=OpenApiParameter.QUERY, required=False, type=int),
        ],
        responses={
            200: PersonSerializer(many=True),
            401: OpenApiResponse(description='Token nao fornecido ou invalido.'),
        },
    ),
    create=extend_schema(
        description='Cria uma nova pessoa com validacoes de cadastro (CPF, CEP, telefone e cidade).',
        request=PersonSerializer,
        examples=[OpenApiExample('Exemplo de request', value=PEOPLE_CREATE_REQUEST_EXAMPLE, request_only=True)],
        responses={
            201: OpenApiResponse(response=PersonSerializer, description='Pessoa criada com sucesso.'),
            400: OpenApiResponse(description='Erro de validacao dos dados enviados.'),
            401: OpenApiResponse(description='Token nao fornecido ou invalido.'),
        },
    ),
    retrieve=extend_schema(
        description='Recupera os dados de uma pessoa pelo identificador.',
        responses={
            200: OpenApiResponse(response=PersonSerializer, description='Pessoa encontrada.', examples=[
                OpenApiExample('Exemplo de resposta', value=PEOPLE_RESPONSE_EXAMPLE)
            ]),
            401: OpenApiResponse(description='Token nao fornecido ou invalido.'),
            404: OpenApiResponse(description='Pessoa nao encontrada.'),
        },
    ),
    update=extend_schema(description='Atualiza totalmente os dados de uma pessoa.'),
    partial_update=extend_schema(description='Atualiza parcialmente os dados de uma pessoa.'),
    destroy=extend_schema(description='Remove uma pessoa quando nao houver bloqueio por relacionamento protegido.'),
)
class PersonViewSet(viewsets.ModelViewSet):
    """API de gerenciamento de pessoas cadastradas na Casa de Apoio."""

    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']
    permission_classes = [IsAuthenticated]
