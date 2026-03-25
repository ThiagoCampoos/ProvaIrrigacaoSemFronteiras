from rest_framework import generics
from people.serializers import UserSerializer
from django.contrib.auth.models import User
from drf_spectacular.utils import extend_schema


@extend_schema(
    description='Cria um novo usuario para autenticacao na API e gera token automaticamente.',
    request=UserSerializer,
    responses={201: UserSerializer},
)
class UserCreate(generics.CreateAPIView):
    """Endpoint publico para criacao de usuario."""

    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer


@extend_schema(
    description='Recupera os dados publicos de um usuario pelo ID.',
    responses={200: UserSerializer},
)
class UserRetrieve(generics.RetrieveAPIView):
    """Endpoint publico para consulta de usuario por identificador."""

    authentication_classes = ()
    permission_classes = ()
    queryset = User.objects.all()
    serializer_class = UserSerializer