#!/bin/sh

set -e

python /usr/src/django-scraper/manage.py makemigrations

python /usr/src/django-scraper/manage.py migrate

# ./manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'adminpass')"

python /usr/src/django-scraper/manage.py runserver 0.0.0.0:8000
