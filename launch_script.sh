#!/bin/sh

set -e

python /usr/src/django-scraper/manage.py makemigrations

python /usr/src/django-scraper/manage.py migrate

python create_user.py

python /usr/src/django-scraper/manage.py runserver 0.0.0.0:8000

celery -A main worker -l info

celery -A main beat -l info
