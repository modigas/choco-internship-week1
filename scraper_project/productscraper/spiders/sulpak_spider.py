import scrapy
import re
from scraper_project.productscraper.items import ProductscraperItem
from products.models import Product

class TechSpiderSulpak(scrapy.Spider):
    name = 'sulpak_tech'
    allowed_domains = ['www.sulpak.kz']
    start_urls = [
                   'https://www.sulpak.kz/f/smartfoniy/nur_sultan',
                   'https://www.sulpak.kz/f/noutbuki/nur_sultan',
                   'https://www.sulpak.kz/f/videokartiy/nur_sultan',
                   'https://www.sulpak.kz/f/processoriy/nur_sultan'
                 ]

    def parse(self, response):
        
        category = response.xpath("//div[@class='breadcrumbs']/ul/li[4]/text()").get()
        products = response.xpath("//div[@class='goods-tiles']")
        for product in products:
            title = product.xpath('normalize-space(.//descendant::h3/text())').get()
            price = product.xpath(".//descendant::div[@class='price']/span/text()").get()
            if price:
                entry = Product(title = title, category = category, price = price, store = 'Sulpak')
                entry.save()
                yield ProductscraperItem(
                    title = title,
                    price = price,
                    category = category,
                    store = 'Sulpak'
                )


        next_page = response.xpath("//a[@class='next']/@href").get()
        next_page_url = f"https://www.sulpak.kz{next_page}"

        if next_page:
            yield scrapy.Request(url=next_page_url, callback=self.parse)
