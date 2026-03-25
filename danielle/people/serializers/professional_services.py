from people.models import ProfessionalServices
from rest_framework import serializers


class ProfessionalServicesSerializer(serializers.ModelSerializer):
    """Serializer para servicos profissionais prestados a pessoas acolhidas."""

    professional_name = serializers.CharField(
        required=False,
        help_text='Somente leitura. Nome do profissional.',
    )
    formatted_created_at = serializers.CharField(
        required=False,
        help_text='Somente leitura. Data de criacao formatada.',
    )

    class Meta:
        model = ProfessionalServices
        exclude = ['updated_at', 'created_at']
        description = 'Serializer para servicos profissionais prestados na Casa de Apoio.'
        extra_kwargs = {
            'professional_name': {'read_only': True},
            'formatted_created_at': {'read_only': True},
            'professional': {'help_text': 'ID da pessoa profissional responsavel pelo atendimento.'},
            'title': {'help_text': 'Titulo do servico (max 120 caracteres).'},
            'description': {'help_text': 'Descricao do servico (max 600 caracteres).'},
        }
