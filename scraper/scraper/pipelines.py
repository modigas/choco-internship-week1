# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import re
import os
from .consts import CATEGORIES
from difflib import SequenceMatcher
from google.cloud import bigquery
from datetime import datetime


table_id = 'precise-antenna-302106.storesitems.products_basemodel'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/usr/src/django-scraper/Choco-Products-Scraper-94e179d2134a.json'

class ScraperPipeline(object):
    """
    Saves Item to the database
    """
    def __init__(self):
        self.client = bigquery.Client()

    def process_item(self, item, spider):
        to_insert = [
            {u"title": item['title'],
             u"category": item['category'],
             u"price": item['price'],
             u"storeName": item['storeName'],
             u"dateAndTime": item['dateAndTime'].timestamp()}
        ]
        err = self.client.insert_rows_json(table_id, to_insert)
        # if err == []:
        #
        # else:
        item.save()
        return item


class TitlePipeline(object):
    """
    Replace text for title with formatted title
    """
    def process_item(self, item, spider):
        if item.get('title'):
            res = ""
            for el in re.finditer(r'[0-9a-zA-Z///.,/-/(/)]+', item['title']):
                res += el.group(0) + ' '
            item['title'] = res.strip()
            return item


class CategoryPipeline(object):
    """

    """
    def process_item(self, item, spider):
        if item.get('category'):
            if '?' in item['category']:
                item['category'] = item['category'].split('?')[0]
            for cat in CATEGORIES:
                sim_ratio = SequenceMatcher(None, cat, item['category']).ratio()
                if sim_ratio >= 0.5:
                    item['category'] = cat
            return item


