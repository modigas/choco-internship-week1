from django.core.management.base import BaseCommand, CommandError
from scrapy.crawler import CrawlerProcess

from scraper_project.productscraper.spiders.sulpak_spider import TechSpiderSulpak
from scraper_project.productscraper.spiders.shopww_spider import TechSpiderShopww
from scraper_project.productscraper.spiders.technodom_spider import TechnodomTechSpider

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        process = CrawlerProcess()
        process.crawl(TechSpiderSulpak)
        process.crawl(TechSpiderShopww)
        # process.crawl(TechnodomTechSpider)
        process.start()