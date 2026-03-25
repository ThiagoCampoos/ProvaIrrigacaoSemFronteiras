from people.models import Person
from rest_framework import serializers
from utils.string.format_text import format_text


class PersonSerializer(serializers.ModelSerializer):
    """Serializer de pessoa com normalizacao textual e campos formatados de leitura."""

    formatted_born_date = serializers.CharField(
        required=False,
        help_text="Somente leitura. Data de nascimento formatada como DD/MM/YYYY.",
    )
    formatted_cpf = serializers.CharField(
        required=False,
        help_text="Somente leitura. CPF formatado como XXX.XXX.XXX-XX.",
    )
    formatted_postal_code = serializers.CharField(
        required=False,
        help_text="Somente leitura. CEP formatado como XXXXX-XXX.",
    )

    def to_internal_value(self, data):
        fields_to_format = [
            'city', 'name', 'mother_name', 'address_line_1', 'address_line_2',
            'neighbourhood'
        ]
        for field in fields_to_format:
            if field in data.keys():
                if data[field]:
                    data[field] = format_text(data[field])
        return super().to_internal_value(data)

    class Meta:
        model = Person
        fields = "__all__"
        description = 'Serializer de pessoa com campos cadastrais e dados formatados de leitura.'
        extra_kwargs = {
            'name': {
                'help_text': 'Nome completo da pessoa (max 100 caracteres).'
            },
            'mother_name': {
                'help_text': 'Nome da mae (opcional).'
            },
            'born_date': {
                'help_text': 'Data de nascimento no formato YYYY-MM-DD.'
            },
            'gender': {
                'help_text': 'Genero: M, F ou O.'
            },
            'cpf': {
                'help_text': 'CPF sem mascara, somente digitos. Exemplo: 12345678901.'
            },
            'rg': {
                'help_text': 'RG da pessoa (opcional).'
            },
            'rg_ssp': {
                'help_text': 'UF emissora do RG (exemplo: SP).'
            },
            'state': {
                'help_text': 'UF de residencia ou origem.'
            },
            'address_line_1': {
                'help_text': 'Endereco principal: rua e numero.'
            },
            'address_line_2': {
                'help_text': 'Complemento de endereco (opcional).'
            },
            'neighbourhood': {
                'help_text': 'Bairro.'
            },
            'city': {
                'help_text': 'Cidade valida no Brasil.'
            },
            'postal_code': {
                'help_text': 'CEP sem mascara, somente digitos. Exemplo: 01310100.'
            },
            'residence_type': {
                'help_text': 'Tipo de residencia: urban ou rural.'
            },
            'ddd_private_phone': {
                'help_text': 'DDD do telefone de contato.'
            },
            'private_phone': {
                'help_text': 'Telefone de contato sem mascara.'
            },
            'ddd_message_phone': {
                'help_text': 'DDD do telefone para mensagem.'
            },
            'message_phone': {
                'help_text': 'Telefone para mensagem sem mascara.'
            },
            'email': {
                'help_text': 'Email valido para contato.'
            },
            'observation': {
                'help_text': 'Observacoes gerais sobre a pessoa (max 600 caracteres).'
            },
            'formatted_born_date': {
                'read_only': True
            },
            'formatted_cpf': {
                'read_only': True
            },
            'formatted_postal_code': {
                'read_only': True
            }
        }
