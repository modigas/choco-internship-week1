import os
from google.cloud import bigquery
from django.core.management.base import BaseCommand


# BaseCommandtable_id = 'precise-antenna-302106.storesitems.products_basemodel'
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/usr/src/django-scraper/Choco-Products-Scraper-94e179d2134a.json'
#
# class Command(BaseCommand):
#     def handle(self, *args, **options):
        # to_insert = [
        #     {u"title": item['title'],
        #      u"category": item['category'],
        #      u"price": item['price'],
        #      u"storeName": item['storeName'],
        #      u"dateAndTime": item['dateAndTime'].timestamp()}
        # ]