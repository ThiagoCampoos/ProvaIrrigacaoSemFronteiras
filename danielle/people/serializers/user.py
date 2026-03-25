from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
import re


class UserSerializer(serializers.ModelSerializer):
    """Serializer para criacao e leitura de usuarios da API."""

    username = serializers.CharField(help_text='Nome de usuario unico para autenticacao.')
    email = serializers.EmailField(required=False, allow_blank=True, help_text='Email de contato do usuario.')
    password = serializers.CharField(write_only=True, help_text='Senha do usuario (somente escrita).')

    def validate_password(self, value):
        return value

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        description = 'Serializer de usuario para cadastro e autenticacao.'
        extra_kwargs = {
            'password': {
                'write_only': True
            },
            'id': {
                'read_only': True,
                'help_text': 'Identificador do usuario.'
            }
        }

    def create(self, validated_data):
        user = User(email=validated_data['email'],
                    username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.is_superuser:
            representation['admin'] = True
        return representation
