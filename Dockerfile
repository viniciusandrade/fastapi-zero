FROM python:3.11-slim
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR app/

RUN pip install poetry
RUN poetry config installer.max-workers 10

COPY pyproject.toml poetry.lock .

RUN poetry install --no-interaction --no-ansi

COPY . .

CMD uvicorn fast_zero.app:app \
    --port 8000 \
    --host 0.0.0.0