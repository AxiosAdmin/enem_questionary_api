FROM python:3.13-slim AS builder

RUN pip install --upgrade pip
RUN pip install poetry
RUN apt-get update && apt-get install -y git & rm -rf /var/lib/apt/lists/*

ENV POETRY_VIRTUALENVS_IN_PROJECT=false
WORKDIR /usr/src/app
COPY pyproject.toml poetry.lock /usr/src/app/

ENV POETRY_REQUESTS_TIMEOUT=120

RUN poetry config virtualenvs.create false && poetry install --no-root --no-cache --no-interaction --no-ansi --verbose

FROM python:3.13-slim

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY . /usr/src/app/