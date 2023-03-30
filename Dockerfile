FROM python:3.10-slim-buster

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY Pipfile Pipfile.lock ./

RUN apt-get update && \
    python -m pip install --upgrade pip && \
    pip install pipenv

RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy
ENV PATH="/.venv/bin:$PATH"

COPY . .
