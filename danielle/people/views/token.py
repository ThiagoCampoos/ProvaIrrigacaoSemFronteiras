from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework import serializers
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

from people.constants import LOGIN_REQUEST_EXAMPLE, LOGIN_RESPONSE_EXAMPLE, LOGIN_ERROR_400_EXAMPLE


class LoginRequestSerializer(serializers.Serializer):
    """Schema do request de autenticacao por usuario e senha."""

    username = serializers.CharField(help_text='Nome de usuario para autenticacao.')
    password = serializers.CharField(help_text='Senha de autenticacao.')


class LoginResponseSerializer(serializers.Serializer):
    """Schema do response de autenticacao com token."""

    token = serializers.CharField(help_text='Token de autenticacao para uso no header Authorization.')
    id = serializers.IntegerField(help_text='ID do usuario autenticado.')


class CustomObtainAuthToken(ObtainAuthToken):
    """Endpoint publico de login que retorna token e id do usuario autenticado."""

    authentication_classes = ()
    permission_classes = ()

    @extend_schema(
        description='Autentica usuario com username e password e retorna token de acesso da API.',
        request=LoginRequestSerializer,
        responses={
            200: OpenApiResponse(
                response=LoginResponseSerializer,
                description='Autenticacao realizada com sucesso.',
                examples=[OpenApiExample('Resposta de sucesso', value=LOGIN_RESPONSE_EXAMPLE)],
            ),
            400: OpenApiResponse(
                description='Credenciais invalidas.',
                examples=[OpenApiExample('Resposta de erro', value=LOGIN_ERROR_400_EXAMPLE)],
            ),
        },
        examples=[
            OpenApiExample('Request de login', value=LOGIN_REQUEST_EXAMPLE, request_only=True),
        ],
    )
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken,
                         self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({
            'token': token.key,
            'id': token.user_id,
        })