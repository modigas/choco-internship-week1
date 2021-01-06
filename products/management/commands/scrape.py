from django.core.management.base import BaseCommand, CommandError
from scrapy.crawler import CrawlerProcess

from scraper_project.productscraper.spiders.store_spider import TechSpider

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        process = CrawlerProcess()
        process.crawl(TechSpider)
        process.start()