FROM python:alpine

WORKDIR /app

EXPOSE 8000

COPY pyproject.toml poetry.lock ./
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    apk add postgresql-client build-base postgresql-dev && \
    poetry install -n --no-root --no-dev

COPY . ./
