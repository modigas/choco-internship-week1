from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from scraper.scraper import settings as my_settings
from scraper.scraper.spiders.products_spider import StoreSpider, BasicSpiderShopWW, BasicSpiderSulpak, SeleniumSpiderTechnodom


class Command(BaseCommand):
    def handle(self, *args, **options):
        crawler_settings = Settings()
        crawler_settings.setmodule(my_settings)
        process = CrawlerProcess(settings=crawler_settings)
        # process.crawl(StoreSpider)
        # process.crawl(BasicSpiderShopWW)
        # process.crawl(BasicSpiderSulpak)
        process.crawl(SeleniumSpiderTechnodom)
        process.start()
