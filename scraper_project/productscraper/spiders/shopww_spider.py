import scrapy
import re
from scraper_project.productscraper.items import ProductscraperItem
from products.models import Product

class TechSpiderShopww(scrapy.Spider):
    name = 'shopww'
    allowed_domains = ['www.shop.kz']
    start_urls = [
        'https://shop.kz/smartfony/filter/almaty-is-v_nalichii-or-ojidaem-or-dostavim/apply/',
        'https://shop.kz/videokarty/filter/nur_sultan-is-v_nalichii-or-ojidaem-or-dostavim/apply/',
        'https://shop.kz/noutbuki/filter/nur_sultan-is-v_nalichii-or-ojidaem-or-dostavim/apply/',
        'https://shop.kz/protsessory/filter/nur_sultan-is-v_nalichii-or-ojidaem-or-dostavim/apply/'
        ]

    def parse(self, response):
        category = response.xpath("//div[@class='bx-breadcrumb']/descendant::span[2]/text()").get()
        products = response.xpath("//div[@class='bx_catalog_item double']")
        for product in products:
            title = product.xpath('.//descendant::a/@title').get()
            price = product.xpath(".//descendant::span[@class='bx-more-price-text']/text()").get()
            if price:
                entry = Product(title = title, category = category, price = price, store = 'ShopWW')
                entry.save()
                yield ProductscraperItem(
                    title = title,
                    price = price,
                    category = category,
                    store = 'ShopWW'
                )

        next_page = response.xpath("//li[@class='bx-pag-next']/a/@href").get()
        next_page_url = f"https://www.shop.kz{next_page}"

        if next_page:
            yield scrapy.Request(url=next_page_url, callback=self.parse)

