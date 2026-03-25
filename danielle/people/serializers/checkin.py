from people.models import Checkin
from rest_framework import serializers

from people.models import PatientCompanionCheckin


class CheckinSerializer(serializers.ModelSerializer):
    """Serializer de check-in com validacao de acompanhante para pacientes."""

    companion_name = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Somente leitura. Nome do acompanhante vinculado.",
    )
    person_name = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Somente leitura. Nome da pessoa principal do check-in.",
    )
    formatted_created_at = serializers.CharField(required=False,
                                                 allow_blank=True,
                                                 help_text="Somente leitura. Data de criacao formatada.")

    def validate(self, data):
        # check if patient have a companion
        if data['reason'] == 'patient':
            if 'companion' not in data.keys():
                raise serializers.ValidationError(
                    {'companion': 'Todo paciente deve ter acompanhante.'})
            else:
                if not data['companion']:
                    raise serializers.ValidationError(
                        {'companion': 'Campo acompanhante não pode ser nulo.'})
        return data

    class Meta:
        model = Checkin
        exclude = ['updated_at', 'created_at']
        description = 'Serializer de check-in com validacoes de negocio para paciente e acompanhante.'
        read_only_fields = ('companion_name', 'person_name',
                            'formatted_created_at')
        extra_kwargs = {
            'person': {
                'help_text': 'ID da pessoa que realizou o check-in.'
            },
            'companion': {
                'help_text': "ID do acompanhante. Obrigatorio quando reason='patient'."
            },
            'reason': {
                'help_text': 'Motivo do check-in: patient, companion, professional, voluntary, visitor ou other.'
            },
            'chemotherapy': {
                'help_text': 'Indica necessidade de quimioterapia.'
            },
            'radiotherapy': {
                'help_text': 'Indica necessidade de radioterapia.'
            },
            'surgery': {
                'help_text': 'Indica necessidade de cirurgia.'
            },
            'exams': {
                'help_text': 'Indica necessidade de exames.'
            },
            'appointment': {
                'help_text': 'Indica necessidade de consulta.'
            },
            'other': {
                'help_text': 'Outras necessidades de atendimento.'
            },
            'ca_number': {
                'help_text': 'Numero C.A. quando aplicavel.'
            },
            'social_vacancy': {
                'help_text': 'Indica se ocupa vaga social.'
            },
            'observation': {
                'help_text': 'Observacoes sobre o check-in (max 600 caracteres).'
            },
            'active': {
                'help_text': 'Status do check-in: true para ativo, false para encerrado.'
            },
        }


class PatientCompanionCheckinSerializer(serializers.ModelSerializer):
    """Serializer para check-in simplificado de paciente com acompanhante."""

    companion_name = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text='Somente leitura. Nome do acompanhante.',
    )
    patient_name = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text='Somente leitura. Nome do paciente.',
    )
    formatted_created_at = serializers.CharField(required=False,
                                                 allow_blank=True,
                                                 help_text='Somente leitura. Data formatada.')

    class Meta:
        model = PatientCompanionCheckin
        exclude = ['updated_at', 'created_at']
        description = 'Serializer de check-in simplificado para vinculo paciente e acompanhante.'
        read_only_fields = ('companion_name', 'patient_name',
                            'formatted_created_at')
        extra_kwargs = {
            'patient': {
                'help_text': 'ID da pessoa paciente.'
            },
            'companion': {
                'help_text': 'ID da pessoa acompanhante.'
            },
        }