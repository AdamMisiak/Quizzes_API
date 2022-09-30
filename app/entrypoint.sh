#!/bin/bash

python manage.py runserver 0.0.0.0:8000
# python manage.py createsuperuser --no-input https://docs.djangoproject.com/en/3.0/ref/django-admin/#django-admin-createsuperuser
#gunicorn -w 4 -b 0.0.0.0:8000 --env DJANGO_SETTINGS_MODULE=core.settings core.wsgi
