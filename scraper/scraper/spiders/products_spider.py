import scrapy
import json
import re

from scraper.scraper import scrape_urls 
from datetime import datetime
from word2number import w2n
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst
from scraper.scraper.items import ScraperItem


class StoreSpider(scrapy.Spider):
    name = 'mechta_tech'
    allowed_domains = ['www.mechta.kz']
    start_urls = ['https://www.mechta.kz/api/main/catalog_new/index.php?section=noutbuki&page_num=1&catalog=true&page_element_count=18',
                  'https://www.mechta.kz/api/main/catalog_new/index.php?section=smartfony&page_num=1&catalog=true&page_element_count=18',
                  'https://www.mechta.kz/api/main/catalog_new/index.php?section=processor&page_num=1&catalog=true&page_element_count=18',
                  'https://www.mechta.kz/api/main/catalog_new/index.php?section=videokarta&page_num=1&catalog=true&page_element_count=18']
    # scrape_urls = scrape_urls.MECHTA_URLS

    max_page_number = 1
    store_name = 'MECHTA'

    def parse(self, response):
        datas = response.xpath('//body/descendant::text()').get()
        JSON = None
        try:
            JSON = json.loads(datas.encode('utf-8'))
        except:
            while True:
                try:
                    ind_start = datas.index('<ifr')
                    ind_end = datas.index('<\/iframe>')
                    chunk = datas[ind_start:ind_end+len('<\/iframe>')]
                    datas = datas.replace(chunk, '')
                except:
                    break
            JSON = json.loads(datas.encode('utf-8'))
        loader = ItemLoader(item=ScraperItem(), response=response)
        loader.default_output_processor = TakeFirst()

        product = JSON['data']['ITEMS']
        total_items = int(JSON['data']['ALL_ITEMS'])
        curr_page = JSON['data']['PAGE_NUMBER']
        category = product[0]["METRICS"]["CATEGORY"]
        max_pages = total_items//18 + 1
        curr_date = datetime.now()

        for elem in product:
            title = elem['NAME']
            price = elem['PRICE']['PRICE']
            loader.add_value('title', title)
            loader.add_value('price', price)
            loader.add_value('category', category)
            loader.add_value('storeName', self.store_name)
            loader.add_value('dateAndTime', curr_date)
            yield loader.load_item()

        if int(curr_page) <= max_pages:
            to_replace = 'page_num=' + str(curr_page)
            replace_with = 'page_num=' + str(int(curr_page) + 1)
            next_page = response.url.replace(to_replace, replace_with)
            yield scrapy.Request(url=next_page, callback=self.parse)


class BasicSpiderShopWW(scrapy.Spider):
    name = 'shopww_tech'
    allowed_domains = ['www.shop.kz']
    start_urls = ['https://shop.kz/smartfony/filter/almaty-is-v_nalichii-or-ojidaem-or-dostavim/apply/',
                  'https://shop.kz/videokarty/filter/nur_sultan-is-v_nalichii-or-ojidaem-or-dostavim/apply/',
                  'https://shop.kz/noutbuki/filter/nur_sultan-is-v_nalichii-or-ojidaem-or-dostavim/apply/',
                  'https://shop.kz/protsessory/filter/nur_sultan-is-v_nalichii-or-ojidaem-or-dostavim/apply/']
    # start_urls = scrape_urls.SHOPWW_URLS

    store_name = 'WHITE WIND'

    def parse(self, response):
        loader = ItemLoader(item=ScraperItem(), response=response)
        loader.default_output_processor = TakeFirst()
        category = response.xpath("//div[@class='bx-breadcrumb']/descendant::span[2]/text()").get()
        products = response.xpath("//div[@class='bx_catalog_item double']")
        for product in products:
            title = product.xpath('.//descendant::a/@title').get()
            price = product.xpath(".//descendant::span[@class='bx-more-price-text']/text()").get()
            if price:
                curr_date = datetime.now()
                loader.add_value('title', title)
                if type(price) == str:
                    loader.add_value('price', scrape_urls.strPriceToNum(price))
                elif type(price) == int:
                    loader.add_value('price', price)
                loader.add_value('category', category)
                loader.add_value('storeName', self.store_name)
                loader.add_value('dateAndTime', curr_date)
                yield loader.load_item()

                # entry = Product(title = title, category = category, price = price, store = 'ShopWW')
                # entry.save()
                # yield ProductscraperItem(
                #     title = title,
                #     price = price,
                #     category = category,
                #     store = 'ShopWW'
                # )

        next_page = response.xpath("//li[@class='bx-pag-next']/a/@href").get()
        next_page_url = f"https://www.shop.kz{next_page}"

        if next_page:
            yield scrapy.Request(url=next_page_url, callback=self.parse)


class BasicSpiderSulpak(scrapy.Spider):
    name = 'sulpak_tech'
    allowed_domains = ['www.sulpak.kz']
    start_urls = ['https://www.sulpak.kz/f/smartfoniy/nur_sultan',
                  'https://www.sulpak.kz/f/noutbuki/nur_sultan',
                  'https://www.sulpak.kz/f/videokartiy/nur_sultan',
                  'https://www.sulpak.kz/f/processoriy/nur_sultan']
    # start_urls = scrape_urls.SULPAK_URLS

    store_name = 'SULPAK'

    def parse(self, response):
        loader = ItemLoader(item=ScraperItem(), response=response)
        loader.default_output_processor = TakeFirst()
        category = response.xpath("//div[@class='breadcrumbs']/ul/li[4]/text()").get()
        products = response.xpath("//div[@class='goods-tiles']")
        for product in products:
            title = product.xpath('normalize-space(.//descendant::h3/text())').get()
            price = product.xpath(".//descendant::div[@class='price']/span/text()").get()
            if price:
                curr_date = datetime.now()
                loader.add_value('title', title)
                if type(price) == str:
                    loader.add_value('price', scrape_urls.strPriceToNum(price))
                elif type(price) == int:
                    loader.add_value('price', price)
                loader.add_value('category', category)
                loader.add_value('storeName', self.store_name)
                loader.add_value('dateAndTime', curr_date)
                yield loader.load_item()
                # entry = Product(title = title, category = category, price = price, store = 'Sulpak')
                # entry.save()
                # yield ProductscraperItem(
                #     title = title,
                #     price = price,
                #     category = category,
                #     store = 'Sulpak'
                # )


        next_page = response.xpath("//a[@class='next']/@href").get()
        next_page_url = f"https://www.sulpak.kz{next_page}"

        if next_page:
            yield scrapy.Request(url=next_page_url, callback=self.parse)


