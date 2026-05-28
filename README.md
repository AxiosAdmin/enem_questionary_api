## Rodando com Docker Compose

O servico `db` usa as variaveis `POSTGRES_DB`, `POSTGRES_USER` e `POSTGRES_PASSWORD` do arquivo `.env` apenas na primeira inicializacao do banco.

Se voce mudar essas credenciais depois que o banco ja foi criado, o Postgres vai continuar usando o estado antigo e podem aparecer erros de autenticacao.

O banco usa um volume externo do Docker chamado `enem_questionary_postgres_data`, entao os dados permanecem mesmo depois de `docker compose down -v`.

Na primeira vez, crie o volume:

```powershell
docker volume create enem_questionary_postgres_data
```

Depois disso, suba a aplicacao normalmente:

```powershell
docker compose up --build
```

## Questoes multimodais e S3

As rotas de geracao de questoes agora persistem a questao no banco e retornam
`support_materials` no payload. Os materiais de apoio podem ser:

- `text` com `inline_text`
- `table` e `chart` com `structured_data`
- `image`, `map`, `diagram` e `infographic` com `generated_image`

Para bancos ja existentes, execute a migration:

```powershell
psql -h <host> -U <user> -d <database> -f src/databases/scripts/1.1_add_question_assets.sql
```

Variaveis novas de ambiente:

- `OPENAI_TEXT_MODEL`
- `OPENAI_IMAGE_MODEL`
- `OPENAI_IMAGE_SIZE`
- `OPENAI_IMAGE_QUALITY`
- `OPENAI_IMAGE_OUTPUT_FORMAT`
- `QUESTION_ASSETS_ENABLE_IMAGE_GENERATION`
- `S3_ENABLED`
- `S3_BUCKET`
- `S3_REGION`
- `S3_ENDPOINT_URL`
- `S3_ACCESS_KEY_ID`
- `S3_SECRET_ACCESS_KEY`
- `S3_PUBLIC_BASE_URL`
- `S3_KEY_PREFIX`

Com `QUESTION_ASSETS_ENABLE_IMAGE_GENERATION=true` e S3 configurado, os assets
visuais sao gerados pela OpenAI e enviados ao bucket. Sem essa configuracao, a
questao ainda e salva, mas o asset visual fica com `storage_status` como
`pending_storage_configuration`, preservando o prompt e os metadados para
ativacao posterior.

Se quiser parar os containers sem mexer nos dados:

```powershell
docker compose down
```

Se quiser apagar o banco local do zero de forma intencional:

```powershell
docker compose down
docker volume rm enem_questionary_postgres_data
docker volume create enem_questionary_postgres_data
docker compose up --build
```
