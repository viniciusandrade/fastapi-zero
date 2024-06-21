FROM python:3.11-slim

ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR app/

RUN pip install poetry

COPY pyproject.toml poetry.lock .

RUN poetry install

COPY . .

CMD uvicorn fast_zero.app:app \
    --port 8000 \
    --host 0.0.0.0