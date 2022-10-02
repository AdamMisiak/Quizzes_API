FROM python:3.10-slim

WORKDIR /app

COPY ./app/entrypoint.sh /app/entrypoint.sh
COPY requirements.txt requirements-dev.txt /app/

RUN pip install -r requirements.txt -r requirements-dev.txt

ENV DJANGO_SETTINGS_MODULE=core.settings
# COPY . /app/