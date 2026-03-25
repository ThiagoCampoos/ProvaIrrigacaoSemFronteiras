# API Casa de Apoio - Recuperacao e Evolucao

Este projeto foi modernizado para execucao local estavel com Django 4.2 LTS, documentacao OpenAPI, seed com Faker, dashboard MVT e mitigacao de N+1.

## Requisitos

- Python 3.10+
- MySQL disponivel localmente
- Dependencias do `requirements.txt`

## Configuracao de ambiente

Copie o arquivo de exemplo para variaveis locais:

```bash
copy .env.example .env
```

Variaveis usadas no banco:

- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`
- `DB_HOST`
- `DB_PORT`

## Setup local (venv)

1. Criar ambiente virtual:

```bash
python -m venv myvenv
```

2. Ativar ambiente virtual (Windows):

```bash
myvenv\Scripts\activate
```

3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

4. Entrar na pasta Django:

```bash
cd danielle
```

5. Aplicar migracoes:

```bash
python manage.py makemigrations
python manage.py migrate
```

6. Criar superusuario (opcional, recomendado para admin):

```bash
python manage.py createsuperuser
```

## Setup alternativo com Docker Compose (MySQL)

Subir apenas o banco com Docker:

```bash
docker compose up -d
```

Depois, executar a aplicacao normalmente via venv (passos da secao anterior).

Parar containers:

```bash
docker compose down
```

## Popular dados

### Fluxo recomendado para testes locais (comando unico)

Prepara o banco local com parametros padrao e limpeza de dados:

```bash
python manage.py seed_local
```

Com migracoes e volume customizado:

```bash
python manage.py seed_local --migrate --people 200 --checkins 160 --home-services 120 --professional-services 90 --checkout-rate 0.4 --seed 2024
```

Manter dados existentes e apenas adicionar novos registros:

```bash
python manage.py seed_local --no-clear --people 20 --checkins 10
```

### Seed estatica (fixtures)

Use sempre caminho completo da fixture:

```bash
python manage.py loaddata people/seed/people.json
python manage.py loaddata people/seed/checkins.json
python manage.py loaddata people/seed/home-services.json
python manage.py loaddata people/seed/professional-services.json
```

### Seed dinamica (Faker)

Execucao padrao:

```bash
python manage.py seed_db --clear
```

Exemplo com volume customizado:

```bash
python manage.py seed_db --clear --people 200 --checkins 160 --home-services 120 --professional-services 90 --checkout-rate 0.4 --seed 2024
```

## Executar aplicacao

```bash
python manage.py runserver
```

## Qualidade (testes e cobertura)

Executar testes:

```bash
pytest
```

Executar cobertura:

```bash
coverage run -m pytest
coverage html
coverage report
```

Meta de qualidade da Fase 4:

- testes passando
- cobertura minima de 75%

## Documentacao da API

- Swagger UI: http://localhost:8000/api/docs/
- ReDoc: http://localhost:8000/api/redoc/
- Schema JSON: http://localhost:8000/api/schema/

## Autenticacao

- `POST /login/` retorna `token` e `id` do usuario.
- Para rotas protegidas, enviar cabecalho:
  - `Authorization: Token <seu_token>`

## Fluxo rapido de uso

1. Criar usuario em `POST /users/`.
2. Autenticar em `POST /login/` para obter token.
3. Consumir rotas em `/api/v1/...` com token no cabecalho.
4. Abrir docs em `/api/docs/`.
5. Ver dashboard em `/dashboard/`.

## Dashboard MVT

- URL: `GET /dashboard/`
- Tipo: pagina server-side (MVT)
- Acesso atual: autenticado por sessao web
- Indicadores:
  - total de check-ins
  - total de check-outs
  - atendimentos ativos
  - percentual de atendimentos ativos
  - distribuicao por servico domestico

## Handoff tecnico (Fase 4)

- Guia de uso da API: `API_USAGE.md`
- Arquitetura e trade-offs: `ARCHITECTURE.md`
- Arguicao e troubleshooting: `TROUBLESHOOTING.md`
- Checklist formal de entrega: `HANDOFF_CHECKLIST.md`
- Acompanhamento macro de tarefas: `task.md`

## Troubleshooting rapido

1. Falha de conexao com MySQL:
   - validar servico ativo, credenciais e permissao de usuario.
2. Erro de modulo nao encontrado:
   - ativar venv correto e reinstalar dependencias.
3. `loaddata` nao encontra arquivo:
   - usar caminho completo da fixture.

## Escopo entregue

- OpenAPI com Swagger/ReDoc
- Dashboard MVT de indicadores
- Seed robusta com Faker
- Melhorias de performance para evitar N+1
