FROM python:alpine

WORKDIR /app

RUN pip install poetry
RUN poetry config virtualenvs.create false
COPY poetry.lock pyproject.toml ./
RUN poetry install -n --no-root --no-dev

COPY . ./
