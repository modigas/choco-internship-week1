import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'productscraper.settings')

app = Celery('send_email')
app.config_from_object('django_config:settings', namespace='CELERY')
app.autodiscover_tasks()