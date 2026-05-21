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
