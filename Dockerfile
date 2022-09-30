FROM python:3.10-slim

WORKDIR /app

COPY ./app/entrypoint.sh /app/entrypoint.sh
COPY requirements.txt /app/

RUN pip install -r requirements.txt

ENV DJANGO_SETTINGS_MODULE=core.settings
# COPY . /app/