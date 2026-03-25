"""Constantes de exemplos para documentacao OpenAPI da API da Casa de Apoio."""

# Choices reutilizaveis em documentacao.
GENDER_CHOICES = ["M", "F", "O"]
STATE_CHOICES = [
    "AC", "AL", "AM", "AP", "BA", "CE", "DF", "ES", "GO", "MA", "MG", "MS", "MT",
    "PA", "PB", "PE", "PI", "PR", "RJ", "RN", "RO", "RR", "RS", "SC", "SE", "SP", "TO",
]
DDD_CHOICES = [
    "11", "21", "31", "41", "47", "48", "51", "61", "62", "63", "65", "67", "71", "79", "81",
    "82", "83", "84", "85", "86", "87", "88", "91", "92", "93", "94", "95", "96", "97", "98",
    "99",
]
CHECKIN_REASON_CHOICES = [
    "patient", "companion", "professional", "voluntary", "visitor", "other",
]

# Exemplos de requests e responses por tipo de operacao CRUD.
PEOPLE_CREATE_REQUEST_EXAMPLE = {
    "name": "Joao Silva Santos",
    "mother_name": "Maria da Silva",
    "born_date": "1985-03-15",
    "gender": "M",
    "email": "joao.silva@email.com",
    "cpf": "12345678901",
    "rg": "1234567",
    "rg_ssp": "SP",
    "state": "SP",
    "address_line_1": "Rua das Flores, 123",
    "address_line_2": "Apartamento 45",
    "neighbourhood": "Centro",
    "city": "Sao Paulo",
    "postal_code": "01310100",
    "residence_type": "urban",
    "ddd_private_phone": "11",
    "private_phone": "33334444",
    "ddd_message_phone": "11",
    "message_phone": "999998888",
    "observation": "Paciente com retorno de consulta em 7 dias.",
}

PEOPLE_RESPONSE_EXAMPLE = {
    "id": 1,
    "name": "Joao Silva Santos",
    "formatted_born_date": "15/03/1985",
    "formatted_cpf": "123.456.789-01",
    "formatted_postal_code": "01310-100",
}

CHECKIN_CREATE_REQUEST_EXAMPLE = {
    "person": 1,
    "companion": 2,
    "reason": "patient",
    "chemotherapy": True,
    "radiotherapy": False,
    "surgery": False,
    "exams": True,
    "appointment": True,
    "other": False,
    "ca_number": "CA-001-2026",
    "social_vacancy": True,
    "observation": "Paciente aguardando atendimento.",
    "active": True,
}

CHECKIN_RESPONSE_EXAMPLE = {
    "id": 10,
    "person": 1,
    "companion": 2,
    "reason": "patient",
    "active": True,
    "person_name": "Joao Silva Santos",
    "companion_name": "Maria Silva",
    "formatted_created_at": "23/03/2026",
}

HOME_SERVICES_CREATE_REQUEST_EXAMPLE = {
    "person": 1,
    "breakfast": True,
    "lunch": True,
    "snack": False,
    "dinner": True,
    "shower": True,
    "sleep": True,
}

HOME_SERVICES_RESPONSE_EXAMPLE = {
    "id": 22,
    "person": 1,
    "person_name": "Joao Silva Santos",
    "breakfast": True,
    "lunch": True,
    "snack": False,
    "dinner": True,
    "shower": True,
    "sleep": True,
    "formatted_created_at": "23/03/2026",
}

PROFESSIONAL_SERVICES_CREATE_REQUEST_EXAMPLE = {
    "professional": 5,
    "title": "Consulta com oncologista",
    "description": "Avaliacao inicial e definicao do plano de cuidado.",
}

PROFESSIONAL_SERVICES_RESPONSE_EXAMPLE = {
    "id": 7,
    "professional": 5,
    "professional_name": "Dr Carlos Medeiros",
    "title": "Consulta com oncologista",
    "description": "Avaliacao inicial e definicao do plano de cuidado.",
    "formatted_created_at": "23/03/2026",
}

PATIENT_COMPANION_CHECKIN_CREATE_REQUEST_EXAMPLE = {
    "patient": 1,
    "companion": 2,
}

PATIENT_COMPANION_CHECKIN_RESPONSE_EXAMPLE = {
    "id": 13,
    "patient": 1,
    "companion": 2,
    "patient_name": "Joao Silva Santos",
    "companion_name": "Maria Silva",
    "formatted_created_at": "23/03/2026",
}

LOGIN_REQUEST_EXAMPLE = {
    "username": "admin",
    "password": "senha123",
}

LOGIN_RESPONSE_EXAMPLE = {
    "token": "abc123def456ghi789",
    "id": 1,
}

LOGIN_ERROR_400_EXAMPLE = {
    "non_field_errors": ["Unable to log in with provided credentials."],
}

# Paginacao e filtros comuns.
LIST_RESPONSE_EXAMPLE = {
    "count": 2,
    "next": "http://localhost:8000/api/v1/people/?limit=12&offset=12",
    "previous": None,
    "results": [PEOPLE_RESPONSE_EXAMPLE],
}

QUERY_PARAM_EXAMPLES = {
    "search": "Joao",
    "ordering_asc": "name",
    "ordering_desc": "-created_at",
    "active_true": "true",
    "active_false": "false",
    "limit": 12,
    "offset": 0,
}

# Padroes de erros esperados por status code.
ERROR_400_EXAMPLE = {
    "cpf": ["CPF invalido"],
    "companion": ["Todo paciente deve ter acompanhante."],
}
ERROR_401_EXAMPLE = {
    "detail": "Authentication credentials were not provided.",
}
ERROR_403_EXAMPLE = {
    "detail": "You do not have permission to perform this action.",
}
ERROR_404_EXAMPLE = {
    "detail": "Not found.",
}
ERROR_500_EXAMPLE = {
    "detail": "Erro interno do servidor.",
}

ERROR_RESPONSES_BY_STATUS = {
    400: ERROR_400_EXAMPLE,
    401: ERROR_401_EXAMPLE,
    403: ERROR_403_EXAMPLE,
    404: ERROR_404_EXAMPLE,
    500: ERROR_500_EXAMPLE,
}
