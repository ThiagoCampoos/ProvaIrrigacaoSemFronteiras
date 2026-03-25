from people.models import HomeServices
from rest_framework import serializers


class HomeServicesSerializer(serializers.ModelSerializer):
    """Serializer para registro de servicos de apoio domestico."""

    person_name = serializers.CharField(
        required=False,
        help_text='Somente leitura. Nome da pessoa atendida.',
    )
    formatted_created_at = serializers.CharField(
        required=False,
        help_text='Somente leitura. Data de criacao formatada.',
    )

    class Meta:
        model = HomeServices
        exclude = ['updated_at', 'created_at']
        description = 'Serializer para servicos de apoio domestico vinculados a uma pessoa.'
        extra_kwargs = {
            'person_name': {'read_only': True},
            'formatted_created_at': {'read_only': True},
            'person': {'help_text': 'ID da pessoa atendida.'},
            'breakfast': {'help_text': 'Indica oferta de cafe da manha.'},
            'lunch': {'help_text': 'Indica oferta de almoco.'},
            'snack': {'help_text': 'Indica oferta de lanche da tarde.'},
            'dinner': {'help_text': 'Indica oferta de jantar.'},
            'shower': {'help_text': 'Indica oferta de banho.'},
            'sleep': {'help_text': 'Indica oferta de pernoite.'},
        }