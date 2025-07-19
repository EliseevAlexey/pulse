FROM python:3.12-slim

ENV POETRY_VERSION=2.1.3 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app

COPY backend/pyproject.toml backend/poetry.lock ./

RUN poetry install --no-root --only main

COPY backend/ .

CMD ["python", "app.py"]
