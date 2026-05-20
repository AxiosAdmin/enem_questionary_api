## Rodando com Docker Compose

O servico `db` usa as variaveis `POSTGRES_DB`, `POSTGRES_USER` e `POSTGRES_PASSWORD` do arquivo `.env` apenas na primeira inicializacao do banco.

Se voce mudar essas credenciais depois que o banco ja foi criado, o Postgres vai continuar usando o estado antigo e podem aparecer erros de autenticacao.

Para recriar o banco local do zero, rode:

```powershell
docker compose down -v
docker compose up --build
```
