FROM python:alpine

WORKDIR /app

EXPOSE 8000

COPY pyproject.toml poetry.lock ./
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install -n --no-root --no-dev

COPY . ./
